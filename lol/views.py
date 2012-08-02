from core.stats import Stats
# from core.spectate import Spectate
from datetime import datetime, timedelta
from django.contrib.auth.decorators import user_passes_test
from django.core.cache import cache
# from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.db.models import Avg
from django.http import HttpResponseRedirect
from coffin.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from models import Summoner, Game, Player, get_data, create_summoner, REGIONS
from pytz import timezone
from tasks import summoner_auto, summoner_auto_task, fill_game, generate_global_stats  # , spectate_check


def __get_region(region):
	return next(value for value, name in REGIONS if name==region.upper())


def __get_region_str(region):
	return next(name for value, name in REGIONS if value==region)


def search(request, name):
	summoners=Summoner.objects.filter(name__iexact=name)
	local=summoners.values()
	for region in range(0, 2):
		if len(filter(lambda row:row['name']==name and row['region']==region, local))==0:
			try:
				res=get_data('search', {'name':name}, __get_region_str(region))
				print res
				if res!={}:
					if not Summoner.objects.filter(account_id=res['account_id'], region=region).exists():
						summoner=create_summoner(res, region)
						summoner_auto(pk=summoner.pk)
					else:
						print Summoner.objects.filter(account_id=res['account_id'], region=region)
			except:
				print 'something broke'
	return render_to_response('search.html.j2', {'summoners':summoners}, RequestContext(request))


# @cache_page(60 * 2)
def game_list(request):
	if 'auto' in request.GET:
		a=Summoner.objects.filter(update_automatically=True)
		b=Player.objects.filter(summoner__in=a, game__fetched=False)
		games=Game.objects.filter(id__in=b.values('game_id'))[:50]
		players=Player.objects.filter(game__in=games).select_related('summoner__name', 'summoner__account_id', 'summoner__region', 'summoner__update_automatically')
	else:
		games=Game.objects.all()[:350]
		players=Player.objects.filter(game__in=games).select_related('summoner__name', 'summoner__account_id', 'summoner__region', 'summoner__update_automatically')
	return render_to_response('game_list.html.j2', {'games':games, 'players':players}, RequestContext(request))


# @cache_page(60 * 60)
def view_game(request, region, game_id):
	region=__get_region(region)
	game=Game.objects.get(game_id=game_id, region=region)
	modes=('CUSTOM', 'BOT', 'UNRANKED', 'RANKED', 'RANKED TEAM', 'RANKED PREMADE')
	metadata={'map':game.get_game_map_display().upper(), 'mode':modes[game.game_mode]}
	if game.fetched==False:
		updating=cache.get('game/{}/{}/filling'.format(game.region, game.game_id))
		if updating!=None:
			if updating.state=='PROGRESS':
				update_in_queue='{:.0%} DONE'.format(float(updating.result['current'])/float(updating.result['total']))
			else:
				update_in_queue='UPDATE IN QUEUE.'
			return render_to_response('view_game.html.j2', {'game':game, 'update_in_queue':update_in_queue, 'metadata':metadata}, RequestContext(request))
		if game.time>(datetime.now(timezone('UTC'))-timedelta(days=2)) and not game.fetched:
			result=fill_game.apply_async(args=[game.pk,], priority=1)
			cache.set('game/{}/{}/filling'.format(game.region, game.game_id), result, 60*10)
			return render_to_response('view_game.html.j2', {'game':game, 'update_in_queue':'UPDATE IN QUEUE.', 'metadata':metadata}, RequestContext(request))
		elif not game.fetched and game.unfetched_players=='':
			game.fetched=True
			game.save()
	if game.blue_team_won:
		players=Player.objects.filter(game=game).order_by('-blue_team', '-gold').select_related()
	else:
		players=Player.objects.filter(game=game).order_by('blue_team', '-gold').select_related()
	if game.game_mode in (3, 4):
		metadata['avg_elo']=players.filter(rating__gt=0).aggregate(Avg('rating'))['rating__avg']
	return render_to_response('view_game.html.j2', {'game':game, 'players':players, 'metadata':metadata}, RequestContext(request))


# @cache_page(60 * 15)
def view_summoner(request, region, account_id, slug):
	sregion=region
	region=__get_region(sregion)
	summoner=Summoner.objects.get(account_id=account_id, region=region)
	needs_update=summoner.needs_update
	if needs_update==True:
		result=summoner_auto_task.apply_async(args=[summoner.pk,], ignore_result=True, priority=0)
		cache.set('summoner/{}/{}/updating'.format(summoner.region, summoner.account_id), result, 60*20)
		update_in_queue='UPDATE IN QUEUE.'
	elif needs_update!=False:
		print type(needs_update)
		update_in_queue=summoner.update_status(needs_update)
	else: update_in_queue=False
	if summoner.slug!=slug: return HttpResponseRedirect(summoner.get_absolute_url())
	rating=summoner.get_rating()
	games=Player.objects.filter(summoner=summoner).select_related()
	stats=cache.get('summoner/{}/{}/stats'.format(summoner.region, summoner.account_id))
	if stats==None:
		stats=Stats(games, summoner_name=summoner.name, cached=True, elo=True)
		stats.generate_index()
		cache.set('summoner/{}/{}/stats'.format(summoner.region, summoner.account_id), stats, 60*60)
	#spectate=cache.get('summoner/{}/{}/spectate'.format(summoner.region, summoner.account_id))
	# if spectate==None:
	# 	result=spectate_check.delay(summoner)
	# 	spectate=Spectate(result, 'summoner/{}/{}/spectate'.format(summoner.region, summoner.account_id))
	# 	cache.set('summoner/{}/{}/spectate'.format(summoner.region, summoner.account_id), spectate, 60*5)
	return render_to_response('view_summoner.html.j2', {'games':games, 'summoner':summoner, 'rating':rating, 'stats':stats, 'update_in_queue':update_in_queue, 'spectate':None}, RequestContext(request))


# @cache_page(60 * 15)
def view_summoner_games(request, region, account_id, slug):
	sregion=region
	region=__get_region(sregion)
	summoner=Summoner.objects.get(account_id=account_id, region=region)
	if summoner.slug!=slug: return HttpResponseRedirect(summoner.get_games_url())
	rating=summoner.get_rating()
	games=Player.objects.filter(summoner=summoner).select_related()
	stats=cache.get('summoner/{}/{}/stats'.format(summoner.region, summoner.account_id))
	if stats==None:
		stats=Stats(games, summoner_name=summoner.name, cached=True, elo=True)
		stats.generate_index()
		cache.set('summoner/{}/{}/stats'.format(summoner.region, summoner.account_id), stats, 60*60)
	return render_to_response('view_summoner_games.html.j2', {'games':Paginator(games, 10).page(1), 'summoner':summoner, 'rating':rating, 'stats':stats}, RequestContext(request))


# @cache_page(60 * 15)
def view_summoner_champions(request, region, account_id, slug):
	from core.champions import CHAMPIONS
	sregion=region
	region=__get_region(sregion)
	summoner=Summoner.objects.get(account_id=account_id, region=region)
	if summoner.slug!=slug: return HttpResponseRedirect(summoner.get_champions_url())
	rating=summoner.get_rating()
	games=Player.objects.filter(summoner=summoner).select_related()
	stats=cache.get('summoner/{}/{}/stats'.format(summoner.region, summoner.account_id))
	if stats==None:
		stats=Stats(games, summoner_name=summoner.name, cached=True, elo=True)
		stats.generate_index(True)
		cache.set('summoner/{}/{}/stats'.format(summoner.region, summoner.account_id), stats, 60*60)
	# assert False
	return render_to_response('view_summoner_champions.html.j2', {'games':games, 'summoner':summoner, 'rating':rating, 'stats':stats, 'champions':CHAMPIONS}, RequestContext(request))


def view_summoner_specific_champion(request, sregion, acctid, slug, champion, champion_slug):
	from core.champions import CHAMPIONS
	region=__get_region(sregion)
	summoner=Summoner.objects.get(account_id=acctid, region=region)
	if slugify(summoner.name)!=slug: return HttpResponseRedirect(reverse('view_summoner_specific_champion', args=[sregion, acctid, slugify(summoner.name), champion, champion_slug]))
	rating=summoner.get_rating()
	games=Player.objects.filter(summoner=summoner, champion_id=champion).select_related()
	stats=Stats(games, champion)
	return render_to_response('view_summoner_specific_champion.html', {'games':games, 'summoner':summoner, 'rating':rating, 'stats':stats, 'champions':CHAMPIONS, 'champion': champion}, RequestContext(request))


# @cache_page(60 * 60)
def view_all_champions(request):
	from core.champions import CHAMPIONS
	from lol.forms import MapModeForm

	form=MapModeForm(request.GET)
	form.is_valid()
	key='global_stats/all'
	games=Player.objects.all().select_related('game__time')
	count=Game.objects.all()
	if form.cleaned_data['game_map'] not in ('', '-1'):
		key+='/'+form.cleaned_data['game_map']
		games=games.filter(game__game_map=form.cleaned_data['game_map'])
		count=count.filter(game_map=form.cleaned_data['game_map'])
	if form.cleaned_data['game_mode'] not in ('', '-1'):
		key+='/'+form.cleaned_data['game_mode']
		games=games.filter(game__game_mode=form.cleaned_data['game_mode'])
		count=count.filter(game_mode=form.cleaned_data['game_mode'])
	stats=cache.get(key)
	if stats==None:
		generating=True
		if cache.get(key+'/generating')==None:
			cache.set(key+'/generating', True, 60*10)
			generate_global_stats.delay(key, games.query, False, display_count=count.count(), champion_history=True)
	else:
		generating=False
	return render_to_response('view_all_champions.html.j2', {'stats':stats, 'champions':CHAMPIONS, 'form':form, 'generating':generating}, RequestContext(request))


# @cache_page(60 * 60)
def view_champion(request, champion_id, champion_slug):
	from core.champions import CHAMPIONS
	from core.items import ITEMS
	from lol.forms import MapModeForm

	champion_id=int(champion_id)
	form=MapModeForm(request.GET)
	form.is_valid()
	key='global_stats/{}'.format(champion_id)
	games=Player.objects.filter(champion_id=champion_id)
	if form.cleaned_data['game_map'] not in ('', '-1'):
		key+='/'+form.cleaned_data['game_map']
		games=games.filter(game__game_map=form.cleaned_data['game_map'])
	if form.cleaned_data['game_mode'] not in ('', '-1'):
		key+='/'+form.cleaned_data['game_mode']
		games=games.filter(game__game_mode=form.cleaned_data['game_mode'])
	stats=cache.get(key)
	if stats==None:
		generating=True
		if cache.get(key+'/generating')==None:
			cache.set(key+'/generating', True, 60*10)
			generate_global_stats.delay(key, games.query, True, champion=champion_id)
	else:
		generating=False
	return render_to_response('view_champion.html.j2', {'stats':stats, 'champion_id':champion_id, 'champion':CHAMPIONS[champion_id], 'items':ITEMS, 'form':form, 'generating':generating}, RequestContext(request))


def run_auto(request):
	if 'force' in request.GET:
		summoners=Summoner.objects.filter(update_automatically=True)
	else:
		summoners=Summoner.objects.filter(update_automatically=True, time_updated__lt=(datetime.utcnow().replace(tzinfo=timezone('UTC'))-timedelta(hours=3)))
	for summoner in summoners:
		summoner_auto_task.delay(summoner.pk)
	if 'fill' in request.GET:
		games=Player.objects.filter(summoner__update_automatically=True, game__fetched=False, game__time__gt=(datetime.utcnow().replace(tzinfo=timezone('UTC'))-timedelta(days=2))).distinct('game').order_by()
		for player in games:
			fill_game.delay(player.game.pk)
	return render_to_response('run_auto.html.j2', {'summoners':summoners}, RequestContext(request))


@user_passes_test(lambda u:u.is_superuser)
def client_status(request):
	server_list=cache.get('servers')
	queue_len=Player.objects.filter(summoner__update_automatically=True, game__fetched=False, game__time__gt=(datetime.utcnow().replace(tzinfo=timezone('UTC'))-timedelta(days=2))).distinct('game').count()
	return render_to_response('client_status.html.j2', {'status':server_list.servers, 'queue_len':queue_len}, RequestContext(request))

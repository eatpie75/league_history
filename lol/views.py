from core.stats import Stats
from datetime import datetime, timedelta
from django import forms
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.db.models import Q, Avg
from django.http import HttpResponseRedirect
# from django.shortcuts import render_to_response
from coffin.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils import simplejson
from models import Summoner, SummonerRating, Game, Player, fill_game, update_summoners, get_data, create_summoner, REGIONS, MAPS, MODES
from pytz import timezone
from tasks import background_update, summoner_auto


def __get_region(region):
	return next(value for value, name in REGIONS if name==region.upper())


def __get_region_str(region):
	return next(name for value, name in REGIONS if value==region)


def __get_rating(summoner):
	try:
		rating=SummonerRating.objects.get(summoner=summoner, game_map=1, game_mode=3)
	except SummonerRating.DoesNotExist:
		rating=SummonerRating(summoner=summoner, game_map=1, game_mode=3, wins=0, losses=0, leaves=0, current_rating=0, top_rating=0)
		rating.save()
	return rating


def search(request, name):
	from django.http import HttpResponse
	local=Summoner.objects.filter(name__iexact=name).values()
	for region in range(0, 2):
		region_str=__get_region_str(region)
		if len(filter(lambda row:row['name']==name and row['region']==region_str, local))==0:
			res=get_data('search', {'name':name}, region_str)
			print res
			if res!={}:
				if not Summoner.objects.filter(account_id=res['account_id'], region=region).exists():
					summoner=create_summoner(res, region)
					update_summoners(Summoner.objects.filter(pk=summoner.pk))
	return HttpResponse(simplejson.dumps(list(Summoner.objects.filter(name__iexact=name).values_list('name', 'level', 'account_id', 'region'))), mimetype='application/json')


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
	if game.time>(datetime.utcnow().replace(tzinfo=timezone('UTC'))-timedelta(days=2)) and not game.fetched:
		fill_game(game)
	if game.blue_team_won:
		# players=game.players.all().order_by('-blue_team', '-gold').select_related('summoner__name', 'summoner__account_id', 'summoner__region')
		players=Player.objects.filter(game=game).order_by('-blue_team', '-gold').select_related()
	else:
		# players=game.players.all().order_by('blue_team', '-gold').select_related('summoner__name', 'summoner__account_id', 'summoner__region')
		players=Player.objects.filter(game=game).order_by('blue_team', '-gold').select_related()
	modes=('CUSTOM', 'BOT', 'UNRANKED', 'RANKED', 'RANKED TEAM', 'RANKED PREMADE')
	metadata={'map':game.get_game_map_display().upper(), 'mode':modes[game.game_mode]}
	if game.game_mode in (3, 4):
		metadata['avg_elo']=players.aggregate(Avg('rating'))['rating__avg']
	return render_to_response('view_game.html.j2', {'game':game, 'players':players, 'metadata':metadata}, RequestContext(request))


# @cache_page(60 * 15)
def view_summoner(request, region, account_id, slug):
	sregion=region
	region=__get_region(sregion)
	summoner=Summoner.objects.get(account_id=account_id, region=region)
	updating=cache.get('{}/{}/updating'.format(summoner.region, summoner.account_id))
	if summoner.time_updated<(datetime.utcnow().replace(tzinfo=timezone('UTC'))-timedelta(hours=1)) and updating==None:
		result=background_update.delay(Summoner.objects.filter(account_id=account_id, region=region))
		cache.set('{}/{}/updating'.format(summoner.region, summoner.account_id), result, 60*20)
		update_in_queue='UPDATE IN QUEUE.'
	elif updating!=None:
		if updating.state=='PENDING':
			update_in_queue='UPDATE IN QUEUE.'
		elif updating.state=='STARTED':
			update_in_queue='UPDATE RUNNING.'
		else:
			update_in_queue='?'
	else: update_in_queue=False
		# summoner=Summoner.objects.get(account_id=account_id, region=region)
	if slugify(summoner.name)!=slug: return HttpResponseRedirect(reverse('view_summoner', args=[sregion, account_id, slugify(summoner.name)]))
	rating=__get_rating(summoner)
	games=Player.objects.filter(summoner=summoner).select_related()
	stats=cache.get('{}/{}/stats'.format(summoner.region, summoner.account_id))
	if stats==None:
		stats=Stats(games, None, summoner.name)
		stats.generate_index()
		cache.set('{}/{}/stats'.format(summoner.region, summoner.account_id), stats, 60*60)
	return render_to_response('view_summoner.html.j2', {'games':games, 'summoner':summoner, 'rating':rating, 'stats':stats, 'update_in_queue':update_in_queue}, RequestContext(request))


# @cache_page(60 * 15)
def view_summoner_games(request, region, account_id, slug):
	sregion=region
	region=__get_region(sregion)
	summoner=Summoner.objects.get(account_id=account_id, region=region)
	if slugify(summoner.name)!=slug: return HttpResponseRedirect(reverse('view_summoner', args=[sregion, account_id, slugify(summoner.name)]))
	rating=__get_rating(summoner)
	games=Player.objects.filter(summoner=summoner).select_related()
	stats=cache.get('{}/{}/stats'.format(summoner.region, summoner.account_id))
	if stats==None:
		stats=Stats(games, None, summoner.name)
		stats.generate_index()
		cache.set('{}/{}/stats'.format(summoner.region, summoner.account_id), stats, 60*60)
	return render_to_response('view_summoner_games.html.j2', {'games':Paginator(games, 10).page(1), 'summoner':summoner, 'rating':rating, 'stats':stats}, RequestContext(request))


# @cache_page(60 * 15)
def view_summoner_champions(request, region, account_id, slug):
	from core.champions import CHAMPIONS
	sregion=region
	region=__get_region(sregion)
	summoner=Summoner.objects.get(account_id=account_id, region=region)
	if slugify(summoner.name)!=slug: return HttpResponseRedirect(reverse('view_summoner_champions', args=[sregion, account_id, slugify(summoner.name)]))
	rating=__get_rating(summoner)
	games=Player.objects.filter(summoner=summoner).select_related()
	stats=cache.get('{}/{}/stats'.format(summoner.region, summoner.account_id))
	if stats==None:
		stats=Stats(games, None, summoner.name)
		stats.generate_index()
		cache.set('{}/{}/stats'.format(summoner.region, summoner.account_id), stats, 60*60)
	# assert False
	return render_to_response('view_summoner_champions.html.j2', {'games':games, 'summoner':summoner, 'rating':rating, 'stats':stats, 'champions':CHAMPIONS}, RequestContext(request))


def view_summoner_specific_champion(request, sregion, acctid, slug, champion, champion_slug):
	from core.champions import CHAMPIONS
	region=__get_region(sregion)
	summoner=Summoner.objects.get(account_id=acctid, region=region)
	if slugify(summoner.name)!=slug: return HttpResponseRedirect(reverse('view_summoner_specific_champion', args=[sregion, acctid, slugify(summoner.name), champion, champion_slug]))
	rating=__get_rating(summoner)
	games=Player.objects.filter(summoner=summoner, champion_id=champion).select_related()
	stats=Stats(games, champion)
	return render_to_response('view_summoner_specific_champion.html', {'games':games, 'summoner':summoner, 'rating':rating, 'stats':stats, 'champions':CHAMPIONS, 'champion': champion}, RequestContext(request))


# @cache_page(60 * 60)
def view_all_champions(request):
	from core.champions import CHAMPIONS

	class MapModeForm(forms.Form):
		maps=[(-1, 'All maps'),]
		maps.extend(MAPS)
		modes=[(-1, 'All modes'),]
		modes.extend(MODES)
		game_map=forms.ChoiceField(required=False, choices=maps[:-1], widget=forms.Select(attrs={'class':'span2'}))
		game_mode=forms.ChoiceField(required=False, choices=modes[:-1], widget=forms.Select(attrs={'class':'span2'}))
	form=MapModeForm(request.GET)
	form.is_valid()
	games=Player.objects.all()
	count=Game.objects.all()
	if form.cleaned_data['game_map'] not in ('', '-1'):
		games=games.filter(game__game_map=form.cleaned_data['game_map'])
		count=count.filter(game_map=form.cleaned_data['game_map'])
	if form.cleaned_data['game_mode'] not in ('', '-1'):
		games=games.filter(game__game_mode=form.cleaned_data['game_mode'])
		count=count.filter(game_mode=form.cleaned_data['game_mode'])
	stats=Stats(games.defer('game'))
	return render_to_response('view_all_champions.html.j2', {'games':games, 'stats':stats, 'champions':CHAMPIONS, 'form':form, 'count':count}, RequestContext(request))


# @cache_page(60 * 60)
def view_champion(request, champion_id, champion_slug):
	from core.champions import CHAMPIONS
	from core.items import ITEMS

	class MapModeForm(forms.Form):
		maps=[(-1, 'All maps'),]
		maps.extend(MAPS)
		modes=[(-1, 'All modes'),]
		modes.extend(MODES)
		game_map=forms.ChoiceField(required=False, choices=maps[:-1], widget=forms.Select(attrs={'class':'span2'}))
		game_mode=forms.ChoiceField(required=False, choices=modes[:-1], widget=forms.Select(attrs={'class':'span2'}))
	form=MapModeForm(request.GET)
	form.is_valid()
	games=Player.objects.filter(champion_id=champion_id)
	count=Game.objects.all()
	if form.cleaned_data['game_map'] not in ('', '-1'):
		games=games.filter(game__game_map=form.cleaned_data['game_map'])
		count=count.filter(game_map=form.cleaned_data['game_map'])
	if form.cleaned_data['game_mode'] not in ('', '-1'):
		games=games.filter(game__game_mode=form.cleaned_data['game_mode'])
		count=count.filter(game_mode=form.cleaned_data['game_mode'])
	stats=Stats(games, champion_id)
	return render_to_response('view_champion.html.j2', {'games':games, 'stats':stats, 'champions':CHAMPIONS, 'items':ITEMS, 'form':form, 'champion':int(champion_id), 'count':count}, RequestContext(request))


def run_auto(request):
	bcount=Summoner.objects.all().count()
	if 'force' in request.GET:
		summoners=Summoner.objects.filter(update_automatically=True)
	else:
		summoners=Summoner.objects.filter(update_automatically=True, time_updated__lt=(datetime.utcnow().replace(tzinfo=timezone('UTC'))-timedelta(hours=3)))
	for summoner in summoners:
		summoner_auto.apply_async(args=[summoner,])
	if 'fill' in request.GET:
		games=Player.objects.filter(summoner__update_automatically=True, game__fetched=False, game__time__gt=(datetime.utcnow().replace(tzinfo=timezone('UTC'))-timedelta(days=2))).distinct('game').order_by()
		for player in games:
			fill_game(player.game)
	acount=Summoner.objects.all().count()
	print "# of new summoners: {}".format(acount-bcount)
	return render_to_response('run_auto.html.j2', {'summoners':summoners}, RequestContext(request))

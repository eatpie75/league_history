# from core.spectate import Spectate
from datetime import datetime, timedelta
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from lol.core.servers import REGIONS
from lol.core.stats import Stats
from lol.models import Summoner, Game, Player, get_data, create_summoner
from lol.tasks import summoner_auto_task, fill_game, generate_global_stats, test_fill, check_servers  # , spectate_check
from lol.utils import EventList, get_cached_value, set_cached_value
from pytz import timezone
import json


def __get_region(region):
	return next(value for value, name in REGIONS if name==region.upper())


def __get_region_str(region):
	return next(name for value, name in REGIONS if value==region)


def search(request, name):
	summoners=Summoner.objects.filter(name__iexact=name).defer('masteries', 'runes')
	local=summoners.values()
	for region in range(0, 2):
		if len(filter(lambda row:row['name'].lower()==name.lower() and row['region']==region, local))==0:
			try:
				res=get_data('search', {'name':name}, __get_region_str(region))
				print res
				if res!={}:
					if not Summoner.objects.filter(account_id=res['account_id'], region=region).exists():
						summoner=create_summoner(res, region)
						summoner_auto_task.delay(summoner.pk)
					else:
						summoner=Summoner.objects.get(account_id=res['account_id'], region=region)
						summoner_auto_task.delay(summoner.pk)
			except:
				print 'something broke'
	summoners=Summoner.objects.filter(name__iexact=name).defer('masteries', 'runes')
	return render_to_response('search.html.j2', {'summoners':summoners}, RequestContext(request))


# @cache_page(60 * 2)
def game_list(request):
	games=Game.objects.all()
	if 'game_map' in request.GET:
		games=games.filter(game_map=request.GET['game_map'])
	if 'fetched' in request.GET:
		games=games.filter(fetched=True)
	if 'auto' in request.GET:
		a=Summoner.objects.filter(update_automatically=True)
		b=Player.objects.filter(summoner__in=a, game__fetched=False)
		games=games.filter(id__in=b.only('game_id').values('game_id'))[:50]
		players=Player.objects.filter(game__in=games).only('game', 'summoner').select_related('summoner__name', 'summoner__account_id', 'summoner__region', 'summoner__update_automatically', 'game__pk')
	else:
		games=games[:50]
		players=Player.objects.filter(game__pk__in=games).only('game', 'summoner').select_related('summoner__name', 'summoner__account_id', 'summoner__region', 'summoner__update_automatically', 'game__pk')
	return render_to_response('game_list.html.j2', {'games':games, 'players':players}, RequestContext(request))


# @cache_page(60 * 60)
def view_game(request, region, game_id):
	region=__get_region(region)
	game=Game.objects.get(game_id=game_id, region=region)
	modes=('CUSTOM', 'BOT', 'UNRANKED', 'RANKED', 'RANKED TEAM', 'RANKED TEAM', 'ARAM', 'ONE FOR ALL', 'SHOWDOWN', 'HEXAKILL', 'URF', 'NIGHTMARE BOT')
	metadata={'map':game.get_game_map_display(), 'mode':modes[game.game_mode], 'ranked':True if game.game_mode in (3,4,5) else False, 'invalid':game.invalid, 'length':-1}
	update_in_queue=False
	if game.fetched is False:
		updating=get_cached_value('game/{}/{}/filling'.format(game.region, game.game_id))
		if updating is not None:
			updating=fill_game.AsyncResult(updating)
			if updating.state=='PROGRESS':
				update_in_queue='{:.0%} DONE'.format(float(updating.result['current']) / float(updating.result['total']))
			else:
				update_in_queue='UPDATE IN QUEUE.'
		if game.time>(datetime.now(timezone('UTC')) - timedelta(days=2)) and not game.fetched:
			fill_game.apply_async(args=[game.pk,], priority=1)
			update_in_queue='UPDATE IN QUEUE.'
		elif not game.fetched and game.unfetched_players=='':
			game.fetched=True
			game.save()
	if game.blue_team_won:
		players=Player.objects.filter(game=game).order_by('-blue_team', '-gold').select_related()
	else:
		players=Player.objects.filter(game=game).order_by('blue_team', '-gold').select_related()
	BASE={
		'num_players':	0,
		'total_elo':	0.0,
		'avg_elo':		0,
		'kills':		0,
		'avg_kills':	0,
		'deaths':		0,
		'avg_deaths':	0,
		'assists':		0,
		'avg_assists':	0,
		'gold':			0,
		'avg_gold':		0,
		'gpm':			0,
		'avg_gpm':		0,
		'cs':			0,
		'avg_cs':		0,
		'pd_dealt':		0,
		'pd_taken':		0,
		'md_dealt':		0,
		'md_taken':		0,
		'td_dealt':		0,
		'td_taken':		0,
		'sw_bought':	0,
		'vw_bought':	0,
		'tw_bought':	0
	}
	metadata['stats']={'winner':BASE.copy(), 'loser':BASE.copy()}
	for player in players:
		team='winner' if player.won else 'loser'
		metadata['stats'][team]['num_players']+=1
		# Begin avg/total stats
		for key, mapping in {'kills':'kills', 'deaths':'deaths', 'assists':'assists', 'minion_kills':'cs', 'neutral_minions_killed':'cs', 'gold':'gold', 'gpm':'gpm'}.iteritems():
			metadata['stats'][team][mapping]+=getattr(player, key)
			metadata['stats'][team]['avg_{}'.format(mapping)]=round(float(metadata['stats'][team][mapping]) / metadata['stats'][team]['num_players'], 1)
		# Begin damage dealt/taken
		metadata['stats'][team]['pd_dealt']+=player.physical_damage_dealt
		metadata['stats'][team]['pd_taken']+=player.physical_damage_taken
		metadata['stats'][team]['md_dealt']+=player.magic_damage_dealt
		metadata['stats'][team]['md_taken']+=player.magic_damage_taken
		metadata['stats'][team]['td_dealt']+=player.damage_dealt
		metadata['stats'][team]['td_taken']+=player.damage_taken
		# Begin wards
		metadata['stats'][team]['sw_bought']+=player.sight_wards_bought_in_game
		metadata['stats'][team]['vw_bought']+=player.vision_wards_bought_in_game
		metadata['stats'][team]['tw_bought']+=player.sight_wards_bought_in_game + player.vision_wards_bought_in_game
		if player.won and metadata['length']==-1:
			metadata['length']=player.length
		# print(u'{}:{}'.format(player.summoner.name, player.length))
		if game.game_mode in (3, 4, 5) and player.tier>0:
			metadata['stats'][team]['total_elo']+=player.rank_to_number
			metadata['stats'][team]['avg_elo']=round(metadata['stats'][team]['total_elo'] / metadata['stats'][team]['num_players'])
	if game.game_mode in (3, 4, 5):
		metadata['avg_elo']=round((metadata['stats']['winner']['avg_elo'] + metadata['stats']['loser']['avg_elo']) / 2)
	chart_data=players.values()
	map(lambda x:x.update(gpm=round(x['gold'] / metadata['length'])) if metadata['length']>0 else x.update(gpm=0), chart_data)
	return render_to_response('view_game.html.j2', {'game':game, 'players':players, 'metadata':metadata, 'update_in_queue':update_in_queue, 'chart_data':json.dumps(list(chart_data))}, RequestContext(request))


def view_summoner_redirect(request, region, account_id):
	sregion=region
	region=__get_region(sregion)
	summoner=Summoner.objects.get(account_id=account_id, region=region)
	return HttpResponseRedirect(summoner.get_absolute_url())


# @cache_page(60 * 15)
def view_summoner(request, region, account_id, slug):
	sregion=region
	region=__get_region(sregion)
	summoner=Summoner.objects.get(account_id=account_id, region=region)
	needs_update=summoner.needs_update
	if needs_update is True:
		summoner_auto_task.apply_async(args=[summoner.pk,], ignore_result=True, priority=0)
		update_in_queue='UPDATE IN QUEUE.'
	elif needs_update is not False:
		task=summoner_auto_task.AsyncResult(needs_update)
		if task.state=='PENDING':
			return 'UPDATE IN QUEUE.'
		elif task.state=='STARTED':
			return 'UPDATE RUNNING.'
		elif task.state=='SUCCESS':
			return False
		else:
			return '?'
	else: update_in_queue=False
	if summoner.slug!=slug:
		return HttpResponseRedirect(summoner.get_absolute_url())
	rating=summoner.get_rating()
	games=Player.objects.filter(summoner=summoner).select_related('game')
	stats=get_cached_value('summoner/{}/{}/stats'.format(summoner.region, summoner.account_id))
	if stats is None:
		stats=Stats(games, summoner_name=summoner.name, summoner_pk=summoner.pk, index_league=True, index_items=False)
		stats.generate_index()
		set_cached_value('summoner/{}/{}/stats'.format(summoner.region, summoner.account_id), stats, 60 * 60)
	# spectate=get_cached_value('summoner/{}/{}/spectate'.format(summoner.region, summoner.account_id))
	# if spectate==None:
	# 	result=spectate_check(summoner)
	# 	spectate=Spectate('summoner/{}/{}/spectate'.format(summoner.region, summoner.account_id))
	# 	spectate.parse(result)
	# 	set_cached_value('summoner/{}/{}/spectate'.format(summoner.region, summoner.account_id), spectate, 60*5)

	return render_to_response('view_summoner.html.j2', {'games':games, 'summoner':summoner, 'rating':rating, 'stats':stats, 'update_in_queue':update_in_queue, 'spectate':None}, RequestContext(request))


# @cache_page(60 * 15)
def view_summoner_games(request, region, account_id, slug):
	sregion=region
	region=__get_region(sregion)
	summoner=Summoner.objects.get(account_id=account_id, region=region)
	if summoner.slug!=slug:
		return HttpResponseRedirect(summoner.get_games_url())
	rating=summoner.get_rating()
	games=Player.objects.filter(summoner=summoner).select_related('game')
	stats=get_cached_value('summoner/{}/{}/stats'.format(summoner.region, summoner.account_id))
	if stats is None:
		stats=Stats(games, summoner_name=summoner.name, index_items=False)
		stats.generate_index()
		set_cached_value('summoner/{}/{}/stats'.format(summoner.region, summoner.account_id), stats, 60 * 60)
	return render_to_response('view_summoner_games.html.j2', {'games':Paginator(games, 10).page(1), 'summoner':summoner, 'rating':rating, 'stats':stats}, RequestContext(request))


# @cache_page(60 * 15)
def view_summoner_champions(request, region, account_id, slug):
	from lol.core.champions import CHAMPIONS
	sregion=region
	region=__get_region(sregion)
	summoner=Summoner.objects.get(account_id=account_id, region=region)
	if summoner.slug!=slug:
		return HttpResponseRedirect(summoner.get_champions_url())
	rating=summoner.get_rating()
	games=Player.objects.filter(summoner=summoner).select_related('game')
	stats=get_cached_value('summoner/{}/{}/stats'.format(summoner.region, summoner.account_id))
	if stats is None:
		stats=Stats(games, summoner_name=summoner.name, index_items=False)
		stats.generate_index()
		set_cached_value('summoner/{}/{}/stats'.format(summoner.region, summoner.account_id), stats, 60 * 60)
	return render_to_response('view_summoner_champions.html.j2', {'games':games, 'summoner':summoner, 'rating':rating, 'stats':stats, 'champions':CHAMPIONS}, RequestContext(request))


def view_summoner_inventory(request, region, account_id, slug):
	sregion=region
	region=__get_region(sregion)
	summoner=Summoner.objects.get(account_id=account_id, region=region)
	if summoner.slug!=slug:
		return HttpResponseRedirect(summoner.get_absolute_url())
	rating=summoner.get_rating()
	games=Player.objects.filter(summoner=summoner).select_related('game')
	stats=get_cached_value('summoner/{}/{}/stats'.format(summoner.region, summoner.account_id))
	if stats is None:
		stats=Stats(games, summoner_name=summoner.name, index_items=False)
		stats.generate_index()
		set_cached_value('summoner/{}/{}/stats'.format(summoner.region, summoner.account_id), stats, 60 * 60)
	return render_to_response('view_summoner_inventory.html.j2', {'summoner':summoner, 'rating':rating, 'stats':stats}, RequestContext(request))


def view_summoner_specific_champion(request, region, account_id, slug, champion, champion_slug):
	from lol.core.champions import CHAMPIONS
	region=__get_region(region)
	summoner=Summoner.objects.get(account_id=account_id, region=region)
	if slugify(summoner.name)!=slug:
		return HttpResponseRedirect(reverse('view_summoner_specific_champion', args=[region, account_id, slugify(summoner.name), champion, champion_slug]))
	rating=summoner.get_rating()
	games=Player.objects.filter(summoner=summoner, champion_id=champion).select_related()
	stats=Stats(games, champion)
	return render_to_response('view_summoner_specific_champion.html', {'games':games, 'summoner':summoner, 'rating':rating, 'stats':stats, 'champions':CHAMPIONS, 'champion': champion}, RequestContext(request))


# @cache_page(60 * 60)
def view_all_champions(request):
	from lol.core.champions import CHAMPIONS
	from lol.forms import MapModeForm

	form=MapModeForm(request.GET)
	form.is_valid()
	key='global_stats/all'
	games=Player.objects.filter(game__time__gt=(datetime.now(timezone('UTC'))) - timedelta(weeks=2)).select_related('game__time')
	count=Game.objects.filter(time__gt=(datetime.now(timezone('UTC'))) - timedelta(weeks=2))
	if form.cleaned_data['game_map'] not in ('', '-1'):
		key+='/' + form.cleaned_data['game_map']
		games=games.filter(game__game_map=form.cleaned_data['game_map'])
		count=count.filter(game_map=form.cleaned_data['game_map'])
	else:
		key+='/-1'
	if form.cleaned_data['game_mode'] not in ('', '-1'):
		key+='/' + form.cleaned_data['game_mode']
		games=games.filter(game__game_mode=form.cleaned_data['game_mode'])
		count=count.filter(game_mode=form.cleaned_data['game_mode'])
	else:
		key+='/-1'
	stats=get_cached_value(key)
	if stats is None:
		generating=True
		if get_cached_value(key + '/generating') is None:
			set_cached_value(key + '/generating', True, 60 * 10)
			generate_global_stats.delay(key, games.query, display_count=count.count(), champion_history=True, global_stats=True, index_items=False)
	else:
		generating=False
	return render_to_response('view_all_champions.html.j2', {'stats':stats, 'champions':CHAMPIONS, 'form':form, 'generating':generating}, RequestContext(request))


# @cache_page(60 * 60)
def view_champion(request, champion_id, champion_slug):
	from lol.core.champions import CHAMPIONS
	from lol.core.items import ITEMS
	from lol.forms import MapModeForm

	champion_id=int(champion_id)
	form=MapModeForm(request.GET)
	form.is_valid()
	key='global_stats/{}'.format(champion_id)
	games=Player.objects.filter(champion_id=champion_id)
	if form.cleaned_data['game_map'] not in ('', '-1'):
		key+='/' + form.cleaned_data['game_map']
		games=games.filter(game__game_map=form.cleaned_data['game_map'])
	else: key+='/-1'
	if form.cleaned_data['game_mode'] not in ('', '-1'):
		key+='/' + form.cleaned_data['game_mode']
		games=games.filter(game__game_mode=form.cleaned_data['game_mode'])
	else: key+='/-1'
	stats=get_cached_value(key)
	if stats is None:
		generating=True
		if get_cached_value(key + '/generating') is None:
			set_cached_value(key + '/generating', True, 60 * 10)
			generate_global_stats.delay(key, games.query, champion=champion_id, champion_history=True, index_items=True)
	else:
		generating=False
	return render_to_response('view_champion.html.j2', {'stats':stats, 'champion_id':champion_id, 'champion':CHAMPIONS[champion_id], 'items':ITEMS, 'form':form, 'generating':generating}, RequestContext(request))


# @cache_page(60 * 60)
def view_champion_items(request, champion_id, champion_slug):
	from lol.core.champions import CHAMPIONS
	from lol.core.items import ITEMS
	from lol.forms import MapModeForm

	champion_id=int(champion_id)
	form=MapModeForm(request.GET)
	form.is_valid()
	key='global_stats/{}'.format(champion_id)
	games=Player.objects.filter(champion_id=champion_id)
	if form.cleaned_data['game_map'] not in ('', '-1'):
		key+='/' + form.cleaned_data['game_map']
		games=games.filter(game__game_map=form.cleaned_data['game_map'])
	else: key+='/-1'
	if form.cleaned_data['game_mode'] not in ('', '-1'):
		key+='/' + form.cleaned_data['game_mode']
		games=games.filter(game__game_mode=form.cleaned_data['game_mode'])
	else: key+='/-1'
	stats=get_cached_value(key)
	if stats is None:
		generating=True
		if get_cached_value(key + '/generating') is None:
			set_cached_value(key + '/generating', True, 60 * 10)
			generate_global_stats.delay(key, games.query, champion=champion_id, champion_history=True, index_items=True)
	else:
		generating=False
	return render_to_response('view_champion_items.html.j2', {'stats':stats, 'champion_id':champion_id, 'champion':CHAMPIONS[champion_id], 'items':ITEMS, 'form':form, 'generating':generating}, RequestContext(request))


@user_passes_test(lambda u:u.is_superuser)
def run_auto(request):
	if 'force' in request.GET:
		summoners=Summoner.objects.filter(update_automatically=True)
	else:
		summoners=Summoner.objects.filter(update_automatically=True, time_updated__lt=(datetime.utcnow().replace(tzinfo=timezone('UTC')) - timedelta(hours=3)))
	if 'fill' in request.GET:
		games=Player.objects.filter(summoner__update_automatically=True, game__fetched=False, game__time__gt=(datetime.utcnow().replace(tzinfo=timezone('UTC')) - timedelta(days=2))).distinct('game').order_by()
		if 'limit' in request.GET:
			games=games[:request.GET['limit']]
		for player in games:
			fill_game.delay(player.game.pk)
	elif 'test' in request.GET:
		test_fill.delay()
	elif 'servers' in request.GET:
		check_servers.delay()
	else:
		for summoner in summoners:
			summoner_auto_task.delay(summoner.pk)
	return render_to_response('run_auto.html.j2', {'summoners':summoners}, RequestContext(request))


@user_passes_test(lambda u:u.is_superuser)
def client_status(request):
	if 'reset_events' in request.GET:
		set_cached_value('event_list', [], timeout=0)
		return HttpResponseRedirect(reverse('lol.views.client_status'))
	server_list=get_cached_value('servers')
	unfetched_games=Player.objects.filter(summoner__update_automatically=True, game__fetched=False, game__time__gt=(datetime.utcnow().replace(tzinfo=timezone('UTC')) - timedelta(days=2))).distinct('game').only('pk').count()
	event_list=EventList(get_cached_value('event_list')).event_list
	return render_to_response('client_status.html.j2', {'status':server_list.servers, 'unfetched_games':unfetched_games, 'event_list':event_list}, RequestContext(request))


@user_passes_test(lambda u:u.is_superuser)
def test_items(request):
	from lol.core.items import ITEMS
	from lol.models import SummonerRating

	summoners=SummonerRating.objects.filter(tier=6, summoner__time_updated__lt=(datetime.now(timezone('UTC')) - timedelta(hours=3)), summoner__region__in=[0, 1]).select_related('summoner').only('summoner__id')
	players=Player.objects.filter(game__fetched=False, game__time__gt=(datetime.now(timezone('UTC')) - timedelta(days=2)), game__region__in=[0, 1], summoner__in=summoners).distinct('game').order_by().only('game')
	# print(len(summoners))
	for wat in players:
		# print(wat.summoner.id, wat.summoner.region)
		pass

	return render_to_response('test_items.html.j2', {'items':ITEMS}, RequestContext(request))

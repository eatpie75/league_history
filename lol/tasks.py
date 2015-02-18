from celery.task import task
from datetime import datetime, timedelta
from django.core.cache import cache
from django.db import transaction
from lol.core.servers import REGIONS
from lol.core.stats import Stats
from lol.models import Summoner, SummonerRating, Player, Game, get_data, parse_games, parse_ratings, parse_summoner, parse_runes, parse_masteries, create_summoner
from lol.utils import log_event, get_cached_value, set_cached_value
from pytz import timezone


@task(ignore_result=True, priority=3)
def auto_update():
	server_list=cache.get('servers')
	available_regions=[next(value for value, name in REGIONS if name==region.upper()) for region in server_list.available_regions]
	summoners=Summoner.objects.filter(update_automatically=True, time_updated__lt=(datetime.now(timezone('UTC')) - timedelta(hours=3)), region__in=available_regions).only('pk', 'region', 'account_id')
	num=0
	for summoner in summoners:
		if get_cached_value('summoner/{}/{}/updating'.format(summoner.region, summoner.account_id)) is None:
			summoner_auto_task.apply_async(args=[summoner.pk,], priority=5)
			num+=1
	log_event('info', datetime.now(timezone('US/Pacific-New')), u'autoupdate added {} summoner(s) to the queue'.format(num))


@task(ignore_result=True, priority=3)
def auto_fill():
	server_list=cache.get('servers')
	available_regions=[next(value for value, name in REGIONS if name==region.upper()) for region in server_list.available_regions]
	games=Player.objects.filter(summoner__update_automatically=True, game__fetched=False, game__time__gt=(datetime.now(timezone('UTC')) - timedelta(days=2)), game__region__in=available_regions).distinct('game').order_by().only('game')
	num=0
	for player in games:
		if get_cached_value('game/{}/{}/filling'.format(player.game.region, player.game.game_id)) is None:
			fill_game.apply_async(args=[player.game.pk,], priority=5)
			num+=1
			log_event('info', datetime.now(timezone('US/Pacific-New')), u'autofill added {} game(s) to the queue'.format(num))


@task(ignore_result=True, priority=5)
def challenger_fill():
	server_list=get_cached_value('servers')
	available_regions=[next(value for value, name in REGIONS if name==region.upper()) for region in server_list.available_regions]
	summoners=SummonerRating.objects.filter(tier=6, summoner__time_updated__lt=(datetime.now(timezone('UTC')) - timedelta(hours=5)), summoner__region__in=available_regions).select_related('summoner').only('summoner__id', 'summoner__region', 'summoner__account_id')
	games=Player.objects.filter(game__fetched=False, game__time__gt=(datetime.now(timezone('UTC')) - timedelta(days=2)), game__region__in=available_regions, summoner__in=summoners).distinct('game').order_by().only('game')
	summoner_num=0
	game_num=0
	for summoner in summoners:
		if get_cached_value('summoner/{}/{}/updating'.format(summoner.summoner.region, summoner.summoner.account_id)) is None:
			summoner_auto_task.apply_async(args=[summoner.summoner.pk,], priority=6)
			summoner_num+=1
	for player in games:
		if get_cached_value('game/{}/{}/filling'.format(player.game.region, player.game.game_id)) is None:
			fill_game.apply_async(args=[player.game.pk,], priority=6)
			game_num+=1
			log_event('info', datetime.now(timezone('US/Pacific-New')), u'challenger fill added {} summoner(s) and {} game(s) to the queue'.format(summoner_num, game_num))


@task(ignore_result=True, priority=3)
def test_fill():
	games=Player.objects.filter(game__fetched=False, game__time__gt=(datetime.now(timezone('UTC')) - timedelta(minutes=30))).distinct('game').order_by()
	for player in games:
		fill_game.apply_async(args=[player.game.pk,], priority=5)


@task(ignore_result=True, priority=1)
def check_servers(**kwargs):
	log_event('info', datetime.now(timezone('US/Pacific-New')), u'checking all servers')
	server_list=get_cached_value('servers')
	server_list.check_servers(up=kwargs.get('up', True), down=kwargs.get('down', True), unknown=kwargs.get('unknown', True))


@task(ignore_result=True, priority=0)
@transaction.atomic
def summoner_auto_task(summoner_pk):
	summoner=Summoner.objects.get(pk=summoner_pk)
	log_event('info', datetime.now(timezone('US/Pacific-New')), u'running autoupdate for:{}'.format(summoner.name), {'type':'summoner', 'summoner':{'region':summoner.region, 'account_id':summoner.account_id, 'name':summoner.name}})
	query={'accounts':summoner.account_id, 'games':1, 'runes':1, 'masteries':1}
	data=get_data('mass_update', query, summoner.get_region_display())['accounts'][0]
	summoner=parse_summoner(data['profile'], summoner)
	summoner=parse_runes(data['runes'], summoner)
	summoner=parse_masteries(data['masteries'], summoner)
	parse_ratings(data['leagues'], summoner)
	if summoner.fully_update:
		parse_games(data['games'], summoner, True)
	else:
		parse_games(data['games'], summoner)
	summoner.time_updated=datetime.now(timezone('UTC'))
	summoner.save()
	cache.delete('summoner/{}/{}/updating'.format(summoner.region, summoner.account_id))
	cache.delete('summoner/{}/{}/stats'.format(summoner.region, summoner.account_id))
	log_event('info', datetime.now(timezone('US/Pacific-New')), u'finished autoupdate for:{}'.format(summoner.name), {'type':'summoner', 'summoner':{'region':summoner.region, 'account_id':summoner.account_id, 'name':summoner.name}})
	return summoner_pk


@task(ignore_result=True, priority=3)
@transaction.atomic
def fill_game(game_pk, auto=False):
	def __parse_queue(queue, query_type, region):
		tmp=[]
		if len(queue)==0:
			return tmp
		while len(queue)>0:
			query={query_type:u','.join(map(unicode, queue[0:5])), 'games':1, 'runes':1, 'masteries':1}
			res=get_data('mass_update', query, region)
			tmp.extend(res['accounts'])
			del queue[0:5]
		return tmp
	game=Game.objects.get(pk=game_pk)
	if not game.fetched and game.unfetched_players!='':
		log_event('info', datetime.now(timezone('US/Pacific-New')), u'filling game: {}/{}'.format(game.region, game.game_id), {'type':'game', 'game':{'region':game.region, 'game_id':game.game_id}})
		tmp=map(int, game.unfetched_players.split(','))
		num_to_fetch=len(tmp)
		summoners=Summoner.objects.filter(summoner_id__in=tmp, region=game.region)
		for s in summoners:
			if s.summoner_id in tmp:
				tmp.remove(s.summoner_id)
		if len(tmp)>0:
			accounts=map(unicode, get_data('get_names', {'ids':u','.join(map(unicode, tmp))}, game.get_region_display()))
		else:
			accounts=[]
		accounts.extend(summoners.values_list('account_id', flat=True))
		res=[]
		res.extend(__parse_queue(filter(lambda v:True if type(v)==int else False, accounts), 'accounts', game.get_region_display()))
		res.extend(__parse_queue(filter(lambda v:True if type(v)==unicode else False, accounts), 'names', game.get_region_display()))
		i=0
		for data in res:
			i+=1
			try:
				summoner=Summoner.objects.get(account_id=data['profile']['account_id'], region=game.region)
				summoner=parse_summoner(data['profile'], summoner)
				summoner=parse_runes(data['runes'], summoner)
				summoner=parse_masteries(data['masteries'], summoner)
			except Summoner.DoesNotExist:
				summoner=create_summoner(data['profile'], game.region)
				summoner=parse_runes(data['runes'], summoner)
				summoner=parse_masteries(data['masteries'], summoner)
			parse_ratings(data['leagues'], summoner)
			if summoner.fully_update and not auto:
				parse_games(data['games'], summoner, True, game)
			else:
				parse_games(data['games'], summoner)
			tmp=game.unfetched_players.split(',')
			if str(summoner.summoner_id) in tmp:
				tmp.remove(str(summoner.summoner_id))
				game.unfetched_players=','.join(tmp)
			summoner.time_updated=datetime.now(timezone('UTC'))
			summoner.save(force_update=True)
			fill_game.update_state(state='PROGRESS', meta={'current':i, 'total':num_to_fetch})
		game.fetched=True
		game.save(force_update=True)
		log_event('info', datetime.now(timezone('US/Pacific-New')), u'finished filling game: {}/{}'.format(game.region, game.game_id), {'type':'game', 'game':{'region':game.region, 'game_id':game.game_id}})
	elif not game.fetched and game.unfetched_players=='':
		log_event('info', datetime.now(timezone('US/Pacific-New')), u'game was already full', {'type':'game', 'game':{'region':game.region, 'game_id':game.game_id}})
		game.fetched=True
		game.save(force_update=True)
	return game_pk


@task(priority=1)
def spectate_check(summoner):
	query={'name':summoner.name, 'full':True}
	res=get_data('spectate', query, summoner.get_region_display())
	return res


@task(ignore_result=True, priority=9)
def generate_global_stats(key, qs, **kwargs):
	log_event('info', datetime.now(timezone('US/Pacific-New')), u'generating global stats with key:{}'.format(key), {'type':'stats', 'args':kwargs})
	new_qs=Player.objects.all()
	new_qs.query=qs
	stats=Stats(new_qs, **kwargs)
	stats.generate_index()
	log_event('info', datetime.now(timezone('US/Pacific-New')), u'generated, caching', {'type':'stats', 'args':kwargs})
	set_cached_value(key, stats, 60 * 60 * 24)
	cache.delete(key + '/generating')
	log_event('info', datetime.now(timezone('US/Pacific-New')), u'finished generating global stats with key:{}'.format(key), {'type':'stats', 'args':kwargs})
	return True

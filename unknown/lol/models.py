from datetime import datetime, timedelta
from django.conf import settings
from django.db import models, transaction
from pytz import timezone
from time import sleep
import random
import requests

MAPS=((0, 'Twisted Treeline'), (1, 'Summoners Rift'), (2, 'Dominion'), (3, '?'))
MODES=((0, 'Custom'), (1, 'Bot'), (2, 'Normal'), (3, 'Solo'), (4, 'Premade'), (5, '?'))
REGIONS=((0, 'NA'), (1, 'EUW'), (2, 'EUNE'))


class Summoner(models.Model):
	region=models.IntegerField(choices=REGIONS, default=0)
	account_id=models.IntegerField(db_index=True)
	summoner_id=models.IntegerField()
	name=models.CharField(max_length=64, db_index=True)
	internal_name=models.CharField(max_length=64)
	level=models.IntegerField()
	profile_icon=models.IntegerField()
	runes=models.TextField(default='', blank=True)
	has_been_updated=models.BooleanField(default=0)
	update_automatically=models.BooleanField(db_index=True, default=False)
	fully_update=models.BooleanField(default=False)
	time_created=models.DateTimeField(auto_now_add=True)
	time_updated=models.DateTimeField(default=datetime.utcnow().replace(tzinfo=timezone('UTC')))

	def __unicode__(self):
		return self.name


class SummonerRankedStatistics(models.Model):
	summoner=models.ForeignKey(Summoner, db_index=True)
	season=models.IntegerField()
	champion_id=models.IntegerField()
	wins=models.IntegerField()
	losses=models.IntegerField()
	kills=models.IntegerField()
	deaths=models.IntegerField()
	assists=models.IntegerField()
	minion_kills=models.IntegerField()
	gold=models.IntegerField()
	turrets_destroyed=models.IntegerField()
	damage_dealt=models.IntegerField()
	physical_damage_dealt=models.IntegerField()
	magical_damage_dealt=models.IntegerField()
	damage_taken=models.IntegerField()
	double_kills=models.IntegerField()
	triple_kills=models.IntegerField()
	quadra_kills=models.IntegerField()
	penta_kills=models.IntegerField()
	time_spent_dead=models.IntegerField()
	maximum_kills=models.IntegerField()
	maximum_deaths=models.IntegerField()


class SummonerRating(models.Model):
	summoner=models.ForeignKey(Summoner, db_index=True)
	game_map=models.IntegerField(choices=MAPS, db_index=True)
	game_mode=models.IntegerField(choices=MODES, db_index=True)
	wins=models.IntegerField()
	losses=models.IntegerField()
	leaves=models.IntegerField()
	current_rating=models.IntegerField(null=True, blank=True)
	top_rating=models.IntegerField(null=True, blank=True)


class Game(models.Model):
	region=models.IntegerField(choices=REGIONS, default=0)
	game_id=models.IntegerField()
	game_map=models.IntegerField(choices=MAPS, db_index=True)
	game_mode=models.IntegerField(choices=MODES, db_index=True)
	time=models.DateTimeField()
	blue_team_won=models.BooleanField()
	players=models.ManyToManyField('Player', related_name='game_players')
	unfetched_players=models.CharField(max_length=128, blank=True)
	fetched=models.BooleanField(default=False)
	# updating=models.BooleanField(default=False)

	def __unicode__(self):
		return unicode(self.time.isoformat())

	class Meta:
		ordering=['-time',]


class Player(models.Model):
	game=models.ForeignKey(Game, db_index=True)
	summoner=models.ForeignKey('Summoner', db_index=True)
	won=models.BooleanField()
	rating=models.IntegerField()
	afk=models.BooleanField()
	leaver=models.BooleanField()
	blue_team=models.BooleanField()
	ping=models.IntegerField()
	queue_length=models.IntegerField()
	premade_size=models.IntegerField()
	experience_earned=models.IntegerField()
	boosted_experience_earned=models.IntegerField()
	ip_earned=models.IntegerField()
	boosted_ip_earned=models.IntegerField()
	summoner_level=models.IntegerField()
	summoner_spell1=models.IntegerField()
	summoner_spell2=models.IntegerField()
	champion_id=models.IntegerField()
	skin_index=models.IntegerField()
	skin_name=models.CharField(max_length=64, null=True, blank=True)
	champion_level=models.IntegerField()
	items=models.CharField(max_length=128)
	kills=models.IntegerField()
	deaths=models.IntegerField()
	assists=models.IntegerField()
	minion_kills=models.IntegerField()
	gold=models.IntegerField()
	damage_dealt=models.IntegerField()
	physical_damage_dealt=models.IntegerField()
	magic_damage_dealt=models.IntegerField()
	damage_taken=models.IntegerField()
	physical_damage_taken=models.IntegerField()
	magic_damage_taken=models.IntegerField()
	total_healing_done=models.IntegerField()
	time_spent_dead=models.IntegerField()
	largest_multikill=models.IntegerField()
	largest_killing_spree=models.IntegerField()
	largest_critical_strike=models.IntegerField()
	neutral_minions_killed=models.IntegerField()
	turrets_destroyed=models.IntegerField()
	inhibitors_destroyed=models.IntegerField()
	nodes_neutralised=models.IntegerField(null=True, blank=True)
	node_neutralisation_assists=models.IntegerField(null=True, blank=True)
	nodes_captured=models.IntegerField(null=True, blank=True)
	victory_points=models.IntegerField(null=True, blank=True)
	objectives=models.IntegerField(null=True, blank=True)
	total_score=models.IntegerField(null=True, blank=True)
	objective_score=models.IntegerField(null=True, blank=True)
	combat_score=models.IntegerField(null=True, blank=True)
	rank=models.IntegerField(null=True, blank=True)

	def _get_items(self):
		return self.items.split('|')[1:-1]
	get_items=property(_get_items)

	def __unicode__(self):
		return unicode(self.summoner.name)

	class Meta:
		ordering=['game',]


def choose_server(region):
	choices=settings.LOL_CLIENT_SERVERS[region]
	return random.choice(choices)


def get_data(url, query, region='NA'):
	server=choose_server(region)
	try:
		res=requests.get('{}/{}/'.format(server, url), params=query, config={'encode_uri':False}, timeout=20.0)
	except requests.exceptions.Timeout:
		print 'got timeout with:{}'.format(query)
		sleep(5)
		print 'retrying'
		res=requests.get('{}/{}/'.format(server, url), params=query, config={'encode_uri':False}, timeout=20.0)
	if res.status_code==500:
		print 'got 500 error with:{}'.format(query)
		sleep(5)
		print 'retrying'
		res=requests.get('{}/{}/'.format(server, url), params=query, config={'encode_uri':False}, timeout=20.0)
	#print res.text
	return res.json


def get_names(query, region='NA'):
	server=choose_server(region)
	try:
		res=requests.get('{}/get_names/'.format(server), params=query, config={'encode_uri':False}, timeout=20.0)
	except requests.exceptions.Timeout:
		print 'got timeout with:{}'.format(query)
		sleep(5)
		print 'retrying'
		res=requests.get('{}/get_names/'.format(server), params=query, config={'encode_uri':False}, timeout=20.0)
	if res.status_code==500:
		print 'got 500 error with:{}'.format(query)
		sleep(5)
		print 'retrying'
		res=requests.get('{}/get_names/'.format(server), params=query, config={'encode_uri':False}, timeout=20.0)
	#print res.text
	return res.json


def update_summoners(all_summoners, games=True, runes=False):
	for region in xrange(0,3):
		# if region==1:
		# 	continue
		summoners=all_summoners.filter(region=region)
		if len(summoners)==0:
			continue
		elif len(summoners)>5:
			print 'running autoupdate for:{}'.format(', '.join(summoners.values_list('name', flat=True)))
			queue=map(unicode, summoners.values_list('account_id', flat=True))
			tmp={}
			while len(queue)>0:
				query={'accounts':u','.join(queue[0:5]), 'games':1}
				res=get_data('mass_update', query, summoners[0].get_region_display())
				tmp.update(res['accounts'])
				for item in queue[0:0+5]:
					queue.remove(item)
				sleep(2)
			res=tmp
		else:
			print 'running autoupdate for:{}'.format(', '.join(summoners.values_list('name', flat=True)))
			query={'accounts':u','.join(map(unicode, summoners.values_list('account_id', flat=True))), 'games':1}
			res=get_data('mass_update', query, summoners[0].get_region_display())['accounts']
		for account, data in res.iteritems():
			summoner=Summoner.objects.get(account_id=int(account))
			if summoner.internal_name!=data['profile']['internal_name']:
				summoner.internal_name=data['profile']['internal_name']
			if summoner.name!=data['profile']['name']:
				summoner.name=data['profile']['name']
			if summoner.level!=data['profile']['level']:
				summoner.level=data['profile']['level']
			if summoner.profile_icon!=data['profile']['profile_icon']:
				summoner.profile_icon=data['profile']['profile_icon']
			parse_ratings(data['stats'], summoner)
			if summoner.fully_update:
				parse_games(data['games'], summoner, True)
			else:
				parse_games(data['games'], summoner)
			summoner.time_updated=datetime.utcnow().replace(tzinfo=timezone('UTC'))
			summoner.save()
	return True


@transaction.commit_on_success
def parse_games(games, summoner, full=False, current=None):
	for ogame in games:
		try:
			game=Game.objects.get(game_id=ogame['id'], region=summoner.region)
			tmp=game.unfetched_players.split(',')
			if str(summoner.summoner_id) in tmp:
				tmp.remove(str(summoner.summoner_id))
				game.unfetched_players=','.join(tmp)
				game.save()
		except Game.DoesNotExist:
			date=datetime.strptime(ogame['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
			date=date.replace(tzinfo=timezone('UTC'))
			game=Game(
				region=summoner.region,
				game_id=ogame['id'],
				time=date
			)
			if ogame['game_type']=='PRACTICE_GAME':
				game.game_mode=0
			elif ogame['queue_type'] in ('RANKED_TEAM_3x3', 'RANKED_TEAM_5x5', 'RANKED_PREMADE_3x3', 'RANKED_PREMADE_5x5'):
				game.game_mode=4
			elif ogame['queue_type'] in ('NORMAL', 'ODIN_UNRANKED'):
				game.game_mode=2
			elif ogame['queue_type']=='RANKED_SOLO_5x5':
				game.game_mode=3
			elif ogame['queue_type']=='BOT':
				game.game_mode=1
			elif ogame['game_type']=='TUTORIAL_GAME':
				continue
			else:
				print ogame['queue_type']
				print ogame['game_mode']
				print ogame['game_type']
			if ogame['game_map'] in (1, 2, 3, 6):
				game.game_map=1
			elif ogame['game_map']==4:
				game.game_map=0
			elif ogame['game_map']==8:
				game.game_map=2
			if (ogame['team']=='blue' and ogame['stats']['win']==1) or (ogame['team']=='purple' and ogame['stats']['win']==0):
				game.blue_team_won=True
			else:
				game.blue_team_won=False
			game.unfetched_players=u','.join(map(unicode, ogame['players']))
			tmp=game.unfetched_players.split(',')
			if str(summoner.summoner_id) in tmp:
				tmp.remove(str(summoner.summoner_id))
				game.unfetched_players=','.join(tmp)
			game.save()
		if not Player.objects.filter(game=game, summoner=summoner):
			try:
				sr=SummonerRating.objects.get(summoner=summoner, game_map=game.game_map, game_mode=game.game_mode)
			except SummonerRating.DoesNotExist:
				sr=SummonerRating(summoner=summoner, game_map=game.game_map, game_mode=game.game_mode, wins=0, losses=0, leaves=0, current_rating=0, top_rating=0)
				sr.save()
			player=Player(
				game=game,
				summoner=summoner,
				rating=sr.current_rating,
				afk=ogame['afk'],
				leaver=ogame['leaver'],
				ping=ogame['ping'],
				queue_length=ogame['queue_length'],
				premade_size=ogame['premade_size'],
				experience_earned=ogame['xp_earned'],
				boosted_experience_earned=ogame['boost_xp'],
				ip_earned=ogame['ip_earned'],
				boosted_ip_earned=ogame['boost_ip'],
				summoner_level=ogame['summoner_level'],
				summoner_spell1=ogame['summoner_spell_one'],
				summoner_spell2=ogame['summoner_spell_two'],
				champion_id=ogame['champion'],
				skin_index=ogame['skin_index'],
				skin_name=ogame['skin_name'],
				champion_level=ogame['stats']['level'],
				kills=ogame['stats']['champions_killed'],
				deaths=ogame['stats']['num_deaths'],
				assists=ogame['stats']['assists'],
				minion_kills=ogame['stats']['minions_killed'],
				gold=ogame['stats']['gold_earned'],
				damage_dealt=ogame['stats']['damage_dealt'],
				physical_damage_dealt=ogame['stats']['physical_damage_dealt_player'],
				magic_damage_dealt=ogame['stats']['magic_damage_dealt_player'],
				damage_taken=ogame['stats']['damage_taken'],
				physical_damage_taken=ogame['stats']['physical_damage_taken'],
				magic_damage_taken=ogame['stats']['magic_damage_taken'],
				total_healing_done=ogame['stats']['total_heal'],
				time_spent_dead=ogame['stats']['total_time_spent_dead'],
				largest_multikill=ogame['stats']['largest_multi_kill'],
				largest_killing_spree=ogame['stats']['largest_killing_spree'],
				largest_critical_strike=ogame['stats']['largest_critical_strike'],
				neutral_minions_killed=ogame['stats']['neutral_minions_killed'],
				turrets_destroyed=ogame['stats']['turrets_killed'],
				inhibitors_destroyed=ogame['stats']['inhibitors_destroyed'],
			)
			if ogame['team']=='blue':
				player.blue_team=True
			else:
				player.blue_team=False
			if (game.blue_team_won and player.blue_team) or (not game.blue_team_won and not player.blue_team):
				player.won=True
			else:
				player.won=False
			items='|'
			for n in xrange(0, 6):
				items+='{}|'.format(ogame['stats']['item{}'.format(n)])
			player.items=items
			player.save()
		else:
			player=Player.objects.get(game=game, summoner=summoner)
		if player not in game.players.all():
			game.players.add(player)
			game.save()
		if not game.fetched and game.time>(datetime.utcnow().replace(tzinfo=timezone('UTC'))-timedelta(days=2)) and full and game!=current:
			print 'Fully updating game:{}'.format(game.game_id)
			print 'For summoner:{}'.format(summoner.name)
			fill_game(game, True)


@transaction.commit_on_success
def parse_summoner(summoner, region=0):
	tmp=Summoner(
		region=region,
		account_id=summoner['account_id'],
		summoner_id=summoner['summoner_id'],
		name=summoner['name'],
		internal_name=summoner['internal_name'],
		level=summoner['level'],
		profile_icon=summoner['profile_icon'],
	)
	tmp.save()
	return tmp


# MAPS=((0, 'Twisted Treeline'), (1, 'Summoners Rift'), (2, 'Dominion'))
# MODES=((0, 'Custom'), (1, 'Bot'), (2, 'Normal'), (3, 'Solo'), (4, 'Premade'))
@transaction.commit_on_success
def parse_ratings(ratings, summoner):
	tmp=SummonerRating.objects.filter(summoner=summoner).select_related()
	for rating in ratings:
		game_type=rating['game_type'].lower()
		game_map=3
		game_mode=5
		if game_type in ('rankedteam5x5', 'rankedpremade5x5'):
			game_mode=4
			game_map=1
		elif  game_type in  ('rankedteam3x3', 'rankedpremade3x3'):
			game_mode=4
			game_map=0
		elif game_type in ('unranked', 'odinunranked'):
			game_mode=2
			game_map=2
		elif game_type=='rankedsolo5x5':
			game_mode=3
			game_map=1
		elif game_type=='coopvsai':
			game_mode=1
			game_map=1
		try:
			rating_model=tmp.get(summoner=summoner, game_mode=game_mode, game_map=game_map)
			rating_model.wins=rating['wins']
			rating_model.losses=rating['losses']
			rating_model.current_rating=rating['rating']
			rating_model.top_rating=rating['rating_max']
		except SummonerRating.DoesNotExist:
			rating_model=SummonerRating(
				summoner=summoner,
				game_map=game_map,
				game_mode=game_mode,
				wins=rating['wins'],
				losses=rating['losses'],
				leaves=rating['leaves'],
				current_rating=rating['rating'],
				top_rating=rating['rating_max']
			)
		rating_model.save()


@transaction.commit_on_success
def fill_game(game, auto=False):
	if not game.fetched and game.unfetched_players!='':
		# unf=map(int, game.unfetched_players.split(','))
		# for sid in unf:
		# 	for pl in Player.objects.filter(game=game, summoner__summoner_id=sid).select_related('summoner').only('summoner__summoner_id'):
		# 		unf.remove(pl.summoner_id)
		names=get_names({'ids':game.unfetched_players}, game.get_region_display())
		accounts=map(unicode, names)
		if len(accounts)>5:
			queue=accounts
			tmp={}
			while len(queue)>0:
				query={'names':u','.join(queue[0:5]), 'games':1}
				res=get_data('mass_update', query, game.get_region_display())
				tmp.update(res['accounts'])
				for item in queue[0:0+5]:
					queue.remove(item)
				sleep(1)
			res=tmp
		else:
			query={'names':u','.join(map(unicode, names)), 'games':1}
			res=get_data('mass_update', query, game.get_region_display())['accounts']
		for account, data in res.iteritems():
			try:
				summoner=Summoner.objects.get(account_id=data['profile']['account_id'], region=game.region)
				parse_ratings(data['stats'], summoner)
			except Summoner.DoesNotExist:
				summoner=parse_summoner(data['profile'], game.region)
				parse_ratings(data['stats'], summoner)
			if summoner.fully_update and not auto:
				parse_games(data['games'], summoner, True, game)
			else:
				parse_games(data['games'], summoner)
			tmp=game.unfetched_players.split(',')
			if str(summoner.summoner_id) in tmp:
				tmp.remove(str(summoner.summoner_id))
				game.unfetched_players=','.join(tmp)
			summoner.time_updated=datetime.utcnow().replace(tzinfo=timezone('UTC'))
			summoner.save()
		game.fetched=True
		game.save()
	elif not game.fetched and game.unfetched_players=='':
		print 'game was already full'
		game.fetched=True
		game.save()
	return True

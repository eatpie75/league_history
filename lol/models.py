from datetime import datetime, timedelta
from django.core.cache import cache
from django.db import models, transaction
from django.utils.text import slugify
from lol.core.servers import prepare_servers, REGIONS
from pytz import timezone
from time import sleep
import requests
import json

MODES=((0, 'Custom'), (1, 'Bot'), (2, 'Normal'), (3, 'Solo'), (4, 'Premade'), (5, 'Team'), (6, 'Aram'), (9, '?'))
MAPS=((0, 'Old Twisted Treeline'), (1, 'Summoners Rift'), (2, 'Dominion'), (3, 'Aram'), (4, 'Twisted Treeline'), (9, '?'))
#{'queue', 'mode', 'map'}
GAME_TYPES={'rankedpremade5x5':(4,1), 'rankedteam5x5':(5,1), 'rankedpremade3x3':(4,4), 'rankedteam3x3':(5,4), 'unranked':(2,1), 'odinunranked':(2,2), 'rankedsolo5x5':(3,1), 'coopvsai':(1,1), 'oldrankedpremade3x3':(4,0), 'oldrankedteam3x3':(5,0)}
RANKED_SOLO_QUEUE_TYPES={'rankedpremade5x5':(5,1), 'rankedpremade3x3':(5,4), 'rankedsolo5x5':(3,1)}
RANKED_GAME_TYPES=((4,1), (5,1), (4,4), (5,4), (3,1))
TIERS=((1, 'BRONZE'), (2, 'SILVER'), (3, 'GOLD'), (4, 'PLATINUM'), (5, 'DIAMOND'), (6, 'CHALLENGER'))
DIVISIONS=((1, 'I'), (2, 'II'), (3, 'III'), (4, 'IV'), (5, 'V'))

prepare_servers()


class Summoner(models.Model):
	region=models.IntegerField(choices=REGIONS, default=0)
	account_id=models.IntegerField(db_index=True)
	summoner_id=models.IntegerField()
	name=models.CharField(max_length=64)
	internal_name=models.CharField(max_length=64)
	level=models.IntegerField()
	profile_icon=models.IntegerField()
	runes=models.TextField(default='{}', blank=True)
	masteries=models.TextField(default='{}', blank=True)
	update_automatically=models.BooleanField(db_index=True, default=False)
	fully_update=models.BooleanField(default=False)
	time_created=models.DateTimeField(auto_now_add=True)
	time_updated=models.DateTimeField(default=datetime.now(timezone('UTC')))
	# time_extra_updated=models.DateTimeField(auto_now_add=True)

	@models.permalink
	def get_absolute_url(self):
		return ('view_summoner', (), {
			'region':self.get_region_display(),
			'account_id':self.account_id,
			'slug':self.slug
		})

	@models.permalink
	def get_games_url(self):
		return ('view_summoner_games', (), {
			'region':self.get_region_display(),
			'account_id':self.account_id,
			'slug':self.slug
		})

	@models.permalink
	def get_champions_url(self):
		return ('view_summoner_champions', (), {
			'region':self.get_region_display(),
			'account_id':self.account_id,
			'slug':self.slug
		})

	def get_runes(self):
		return json.loads(self.runes)

	def get_masteries(self):
		return json.loads(self.masteries)

	def get_rating(self):
		try:
			rating=SummonerRating.objects.get(summoner=self, game_map=1, game_mode=3)
		except SummonerRating.DoesNotExist:
			rating=SummonerRating(summoner=self, game_map=1, game_mode=3, wins=0, losses=0)
			rating.save()
		return rating

	@property
	def needs_update(self):
		if self.time_updated<(datetime.now(timezone('UTC'))-timedelta(hours=1)):
			updating=cache.get('summoner/{}/{}/updating'.format(self.region, self.account_id))
			if updating is not None:
				return updating
			else:
				return True
		else:
			return False

	@property
	def slug(self):
		return slugify(self.name) if len(slugify(self.name))>0 else '-'

	def __unicode__(self):
		return self.name

	class Meta:
		index_together=[
			("region", "account_id"),
		]
		unique_together=(("region", "account_id"))


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
	game_map=models.IntegerField(choices=MAPS, db_index=True, null=False)
	game_mode=models.IntegerField(choices=MODES, db_index=True, null=False)
	wins=models.IntegerField()
	losses=models.IntegerField()
	league=models.CharField(max_length=127, null=True, blank=True)
	tier=models.IntegerField(choices=TIERS, null=True, blank=True)
	division=models.IntegerField(choices=DIVISIONS, null=True, blank=True)
	rank=models.IntegerField(null=True, blank=True)
	miniseries_target=models.IntegerField(default=0)
	miniseries_wins=models.IntegerField(default=0)
	miniseries_losses=models.IntegerField(default=0)

	@property
	def rank_to_number(self):
		return rank_to_number(self.tier, self.division, self.rank)

	class Meta:
		index_together=[
			("summoner", "game_map", "game_mode")
		]
		unique_together=(("summoner", "game_map", "game_mode"))


class Game(models.Model):
	region=models.IntegerField(choices=REGIONS, default=0)
	game_id=models.IntegerField()
	game_map=models.IntegerField(choices=MAPS, db_index=True)
	game_mode=models.IntegerField(choices=MODES, db_index=True)
	time=models.DateTimeField(db_index=True)
	blue_team_won=models.BooleanField()
	invalid=models.BooleanField(default=False)
	unfetched_players=models.CharField(max_length=128, blank=True)
	fetched=models.BooleanField(default=False)

	@models.permalink
	def get_absolute_url(self):
		return ('view_game', (), {
			'region':self.get_region_display(),
			'game_id':self.game_id,
		})

	def __unicode__(self):
		return unicode(self.time.isoformat())

	class Meta:
		ordering=['-time',]
		index_together=[
			("game_map", "game_mode"),
			("game_id", "region")
		]
		unique_together=(("region", "game_id"))


class Player(models.Model):
	game=models.ForeignKey(Game, db_index=True)
	summoner=models.ForeignKey('Summoner', db_index=True)

	won=models.BooleanField()

	tier=models.IntegerField(choices=TIERS, null=True, blank=True)
	division=models.IntegerField(choices=DIVISIONS, null=True, blank=True)
	rank=models.IntegerField(null=True, blank=True)

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

	neutral_minions_killed=models.IntegerField()
	neutral_minions_killed_your_jungle=models.IntegerField()
	neutral_minions_killed_enemy_jungle=models.IntegerField()

	gold=models.IntegerField()

	physical_damage_dealt=models.IntegerField()
	magic_damage_dealt=models.IntegerField()
	true_damage_dealt=models.IntegerField()
	damage_dealt=models.IntegerField()

	physical_damage_taken=models.IntegerField()
	magic_damage_taken=models.IntegerField()
	true_damage_taken=models.IntegerField()
	damage_taken=models.IntegerField()

	total_time_crowd_control_dealt=models.IntegerField()
	total_healing_done=models.IntegerField()
	time_spent_dead=models.IntegerField()

	largest_multikill=models.IntegerField()
	largest_killing_spree=models.IntegerField()
	largest_critical_strike=models.IntegerField()

	turrets_destroyed=models.IntegerField()
	inhibitors_destroyed=models.IntegerField()

	sight_wards_bought_in_game=models.IntegerField()
	vision_wards_bought_in_game=models.IntegerField()
	ward_placed=models.IntegerField()
	ward_killed=models.IntegerField()

	node_neutralize=models.IntegerField(null=True, blank=True)
	node_neutralize_assist=models.IntegerField(null=True, blank=True)
	node_capture=models.IntegerField(null=True, blank=True)
	node_capture_assist=models.IntegerField(null=True, blank=True)
	victory_point_total=models.IntegerField(null=True, blank=True)
	team_objective=models.IntegerField(null=True, blank=True)
	total_player_score=models.IntegerField(null=True, blank=True)
	objective_player_score=models.IntegerField(null=True, blank=True)
	combat_player_score=models.IntegerField(null=True, blank=True)
	total_score_rank=models.IntegerField(null=True, blank=True)

	@property
	def get_items(self):
		return self.items.split('|')[1:-1]

	@property
	def length(self):
		ip=self.ip_earned-self.boosted_ip_earned if self.ip_earned-self.boosted_ip_earned<=145 else (self.ip_earned-self.boosted_ip_earned)-150
		if self.game.game_mode not in (2, 3, 4, 5): return 0
		if self.game.game_map in (1,4):  # classic, twisted treeline
			base=18 if self.won else 16
			mingain=2.26975458333333 if self.won else 1.38803291666667
			max_length=55
			if (self.won and ip==76) or (not self.won and ip==51):
				result=25
			elif (self.won and ip>=145) or (not self.won and ip>=94):
				result=55
			else:
				# result=round((ip-base)/mingain, 1)
				result=(ip-base)/mingain
		elif self.game.game_map==2:  # dominion
			base=20 if self.won else 12
			mingain=2 if self.won else 1
			max_length=55
			result=(ip-base)/mingain
		return result if result<=max_length else max_length

	@property
	def gpm(self):
		if self.length>0:
			return round(self.gold/self.length)
		else:
			return 0

	@property
	def rank_to_number(self):
		return rank_to_number(self.tier, self.division, self.rank)

	@models.permalink
	def get_absolute_url(self):
		return ('view_game', (), {
			'region':self.game.get_region_display(),
			'game_id':self.game.game_id,
		})

	def __unicode__(self):
		return unicode(self.summoner.name)

	class Meta:
		ordering=['game',]
		unique_together=(("game", "summoner"))


class ClientEmuError(Exception):
	pass


def get_data(url, query, region='NA'):
	servers=cache.get('servers')
	server_data=servers.choose_server(region)
	server=server_data['url']
	# print 'using server:{}'.format(server)

	def _attempt(server, url):
		try:
			res=requests.get('{}/{}/'.format(server, url), params=query, timeout=20.0)
		except (requests.exceptions.Timeout, requests.packages.urllib3.exceptions.MaxRetryError, requests.packages.urllib3.exceptions.TimeoutError) as e:
			res=e
		return res
	res=_attempt(server, url)
	if type(res) in (requests.exceptions.Timeout, requests.packages.urllib3.exceptions.TimeoutError, requests.packages.urllib3.exceptions.MaxRetryError):
		print 'got timeout on:{} - with query:{}'.format(server, query)
		sleep(5)
		print 'retrying'
		server_data=servers.check_servers([{'url':server, 'region':region},])
		server=server_data['url']
		res=_attempt(server, url)
		if type(res) in (requests.exceptions.Timeout, requests.packages.urllib3.exceptions.TimeoutError, requests.packages.urllib3.exceptions.MaxRetryError):
			print 'second error'
			raise ClientEmuError()
		elif res.status_code==500:
			raise ClientEmuError()
	elif res.status_code==500:
		print 'got 500 error on:{} - with query:{}'.format(server, query)
		sleep(5)
		print 'retrying'
		server_data=servers.check_servers([{'url':server, 'region':region},])
		server=server_data['url']
		res=_attempt(server, url)
		if res in (requests.exceptions.Timeout, requests.packages.urllib3.exceptions.TimeoutError, requests.packages.urllib3.exceptions.MaxRetryError):
			print 'second error'
			raise ClientEmuError()
		elif res.status_code==500:
			raise ClientEmuError()
	res=res.json()
	ids=server_data['metadata'].get('ids', [])
	if res['server'] not in ids:
		ids.append(res['server'])
		servers.set_metadata(region, server, {'ids':ids})
	return res['data']


@transaction.commit_on_success
def parse_games(games, summoner, full=False, current=None):
	for ogame in games:
		try:
			game=Game.objects.get(game_id=ogame['id'], region=summoner.region)
			if game.fetched:
				continue
			tmp=game.unfetched_players.split(',')
			if str(summoner.summoner_id) in tmp:
				tmp.remove(str(summoner.summoner_id))
				game.unfetched_players=','.join(tmp)
				game.save(force_update=True)
		except Game.DoesNotExist:
			date=datetime.strptime(ogame['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
			date=date.replace(tzinfo=timezone('UTC'))
			game=Game(
				region=summoner.region,
				game_id=ogame['id'],
				time=date,
				invalid=ogame['invalid']
			)
			if ogame['game_type']=='PRACTICE_GAME':
				game.game_mode=0
			elif ogame['queue_type'] in ('BOT', 'BOT_3x3'):
				game.game_mode=1
			elif ogame['queue_type'] in ('NORMAL', 'NORMAL_3x3', 'ODIN_UNRANKED'):
				game.game_mode=2
			elif ogame['queue_type']=='RANKED_SOLO_5x5':
				game.game_mode=3
			elif ogame['queue_type'] in ('RANKED_PREMADE_3x3', 'RANKED_PREMADE_5x5'):
				game.game_mode=4
			elif ogame['queue_type'] in ('RANKED_TEAM_3x3', 'RANKED_TEAM_5x5'):
				game.game_mode=5
			elif ogame['game_mode']=='ARAM' and (ogame['game_type']=='CUSTOM_GAME' or ogame['queue_type']=='ARAM_UNRANKED_5x5'):
				game.game_mode=6
			elif ogame['queue_type']=='NONE' and ogame['game_type']=='CUSTOM_GAME':
				game.game_mode=0
			elif ogame['game_type']=='TUTORIAL_GAME':
				continue
			else:
				print 'couldn\'t figure out game mode for game #{}'.format(game.game_id)
				print('queue_type:"{}", game_mode:"{}", game_type:"{}", game_map:"{}"'.format(ogame['queue_type'], ogame['game_mode'], ogame['game_type'], ogame['game_map']))
			if ogame['game_map'] in (1, 2, 3, 6):
				game.game_map=1
			elif ogame['game_map']==8:
				game.game_map=2
			elif ogame['game_map'] in (7, 12):
				game.game_map=3
			elif ogame['game_map']==10:
				game.game_map=4
			elif ogame['game_map']==4:
				game.game_map=0
			else:
				print 'couldn\'t figure out game map for game #{}'.format(game.game_id)
				print('queue_type:"{}", game_mode:"{}", game_type:"{}", game_map:"{}"'.format(ogame['queue_type'], ogame['game_mode'], ogame['game_type'], ogame['game_map']))
			if (ogame['team']=='blue' and ogame['stats']['win']==1) or (ogame['team']=='purple' and ogame['stats']['win']==0):
				game.blue_team_won=True
			else:
				game.blue_team_won=False
			game.unfetched_players=u','.join(map(unicode, ogame['players']))
			tmp=game.unfetched_players.split(',')
			if str(summoner.summoner_id) in tmp:
				tmp.remove(str(summoner.summoner_id))
				game.unfetched_players=','.join(tmp)
			game.save(force_insert=True)
		if not Player.objects.filter(game=game, summoner=summoner).exists():
			try:
				sr=SummonerRating.objects.get(summoner=summoner, game_map=game.game_map, game_mode=game.game_mode)
				tier=sr.tier
				division=sr.division
				rank=sr.rank
			except SummonerRating.DoesNotExist:
				tier=0
				division=0
				rank=0
			player=Player(
				game=game,
				summoner=summoner,
				
				tier=tier, division=division, rank=rank,

				afk=ogame['afk'], leaver=ogame['leaver'],

				ping=ogame['ping'],	queue_length=ogame['queue_length'],	premade_size=ogame['premade_size'],

				experience_earned=ogame['xp_earned'], boosted_experience_earned=ogame['boost_xp'],

				ip_earned=ogame['ip_earned'], boosted_ip_earned=ogame['boost_ip'],

				summoner_level=ogame['summoner_level'],

				summoner_spell1=ogame['summoner_spell_one'], summoner_spell2=ogame['summoner_spell_two'],

				champion_id=ogame['champion'],
				skin_index=ogame['skin_index'], skin_name=ogame['skin_name'],

				champion_level=ogame['stats']['level'],

				kills=ogame['stats']['champions_killed'],
				deaths=ogame['stats']['num_deaths'],
				assists=ogame['stats']['assists'],

				minion_kills=ogame['stats']['minions_killed'],

				neutral_minions_killed=ogame['stats']['neutral_minions_killed'],
				neutral_minions_killed_your_jungle=ogame['stats']['neutral_minions_killed_your_jungle'],
				neutral_minions_killed_enemy_jungle=ogame['stats']['neutral_minions_killed_enemy_jungle'],

				gold=ogame['stats']['gold_earned'],

				physical_damage_dealt=ogame['stats']['physical_damage_dealt_to_champions'],
				magic_damage_dealt=ogame['stats']['magic_damage_dealt_to_champions'],
				true_damage_dealt=ogame['stats']['true_damage_dealt_to_champions'],
				damage_dealt=ogame['stats']['total_damage_dealt_to_champions'],

				physical_damage_taken=ogame['stats']['physical_damage_taken'],
				magic_damage_taken=ogame['stats']['magic_damage_taken'],
				true_damage_taken=ogame['stats']['true_damage_taken'],
				damage_taken=ogame['stats']['total_damage_taken'],

				total_time_crowd_control_dealt=ogame['stats']['total_time_crowd_control_dealt'],
				total_healing_done=ogame['stats']['total_heal'],
				time_spent_dead=ogame['stats']['total_time_spent_dead'],

				largest_multikill=ogame['stats']['largest_multi_kill'],
				largest_killing_spree=ogame['stats']['largest_killing_spree'],
				largest_critical_strike=ogame['stats']['largest_critical_strike'],

				turrets_destroyed=ogame['stats']['turrets_killed'],
				inhibitors_destroyed=ogame['stats']['barracks_killed'],

				sight_wards_bought_in_game=ogame['stats']['sight_wards_bought_in_game'],
				vision_wards_bought_in_game=ogame['stats']['vision_wards_bought_in_game'],
				ward_placed=ogame['stats']['ward_placed'],
				ward_killed=ogame['stats']['ward_killed'],

				node_neutralize=ogame['stats']['node_neutralize'], node_neutralize_assist=ogame['stats']['node_neutralize_assist'],
				node_capture=ogame['stats']['node_capture'], node_capture_assist=ogame['stats']['node_capture_assist'],
				victory_point_total=ogame['stats']['victory_point_total'],
				team_objective=ogame['stats']['team_objective'],
				objective_player_score=ogame['stats']['objective_player_score'], combat_player_score=ogame['stats']['combat_player_score'], total_player_score=ogame['stats']['total_player_score'],
				total_score_rank=ogame['stats']['total_score_rank']
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
			player.save(force_insert=True)
		else:
			player=Player.objects.get(game=game, summoner=summoner)
	transaction.commit()


@transaction.commit_on_success
def create_summoner(summoner, region=0):
	tmp=Summoner(
		region=region,
		account_id=summoner['account_id'],
		summoner_id=summoner['summoner_id'],
		name=summoner['name'],
		internal_name=summoner['internal_name'],
		level=summoner['level'],
		profile_icon=summoner['profile_icon'],
	)
	tmp.save(force_insert=True)
	ratings=[]
	for game_type, values in RANKED_SOLO_QUEUE_TYPES.iteritems():
		ratings.append(
			SummonerRating(
				summoner=tmp,
				game_mode=values[0],
				game_map=values[1],
				wins=0,
				losses=0
			)
		)
	SummonerRating.objects.bulk_create(ratings)
	return tmp


def parse_summoner(data, summoner):
	if summoner.internal_name!=data['internal_name']:
		summoner.internal_name=data['internal_name']
	if summoner.name!=data['name']:
		summoner.name=data['name']
	if summoner.level!=data['level']:
		summoner.level=data['level']
	if summoner.profile_icon!=data['profile_icon']:
		summoner.profile_icon=data['profile_icon']
	return summoner


@transaction.commit_on_success
def parse_ratings(ratings, summoner):
	# MAPS=((0, 'Old Twisted Treeline'), (1, 'Summoners Rift'), (2, 'Dominion'), (3, 'Aram'), (4, 'Twisted Treeline'), (9, '?'))
	# MODES=((0, 'Custom'), (1, 'Bot'), (2, 'Normal'), (3, 'Solo'), (4, 'Premade'), (5, 'Team'), (6, 'Aram'), (9, '?'))
	# RANKED_SOLO_QUEUE_TYPES={'rankedpremade5x5':(4,1), 'rankedteam5x5':(5,1), 'rankedpremade3x3':(4,4), 'rankedteam3x3':(5,4), 'rankedsolo5x5':(3,1)}
	pre_ratings=SummonerRating.objects.filter(summoner=summoner)
	for rating in ratings:
		if rating['queue'].replace('_', '').lower() in RANKED_SOLO_QUEUE_TYPES:
			game_mode, game_map=RANKED_SOLO_QUEUE_TYPES[rating['queue'].replace('_', '').lower()]
		else:
			continue
		# print(rating)
		tmp=pre_ratings.get_or_create(game_mode=game_mode, game_map=game_map, defaults={'summoner':summoner, 'wins':rating['wins'], 'losses':rating['losses']})
		if tmp[1]==0:
			r=tmp[0]
			if r.wins!=int(rating['wins']) or r.losses!=int(rating['losses']) or r.rank!=int(rating['league_rank']) or r.league!=rating['name'] or r.tier!=rating['tier'] or r.division!=int(rating['rank']):
				r.wins=rating['wins']
				r.losses=rating['losses']
				r.rank=rating['league_rank']
				r.league=rating['name']
				r.tier=rating['tier']
				r.division=rating['rank']
				if rating['mini_series'] is None:
					r.miniseries_target=0
					r.miniseries_wins=0
					r.miniseries_losses=0
				else:
					r.miniseries_target=rating['mini_series']['target']
					r.miniseries_wins=rating['mini_series']['wins']
					r.miniseries_losses=rating['mini_series']['losses']
				r.save(force_update=True)


def parse_masteries(masteries, summoner):
	summoner.masteries=json.dumps(masteries)
	return summoner


def parse_runes(runes, summoner):
	summoner.runes=json.dumps(runes)
	return summoner


def rank_to_number(tier, division, rank):
	num=(500*(tier-1))+(100*(5-division))+(100-rank)
	if tier==6:
		num-=450
	return num


def number_to_rank(number):
	tier=number//500+1
	division=(number-(tier-1)*500)//100
	rank=100-(number-(tier-1)*500-division*100)
	if tier==6:
		division=4
		rank-=50
	return {'tier':tier, 'division':5-division, 'rank':rank}

from datetime import datetime, timedelta
from django.core.cache import cache
from django.db import models, transaction
from django.template.defaultfilters import slugify
from pytz import timezone
from time import sleep
import requests
import simplejson

MAPS=((0, 'Twisted Treeline'), (1, 'Summoners Rift'), (2, 'Dominion'), (3, 'Aram'), (9, '?'))
MODES=((0, 'Custom'), (1, 'Bot'), (2, 'Normal'), (3, 'Solo'), (4, 'Premade'), (5, 'Team'), (6, 'Aram'), (9, '?'))
GAME_TYPES={'RankedPremade5x5':(4,1), 'RankedTeam5x5':(5,1), 'RankedPremade3x3':(4,0), 'RankedTeam3x3':(5,0), 'Unranked':(2,1), 'OdinUnranked':(2,2), 'RankedSolo5x5':(3,1), 'CoopVsAi':(1,1)}
REGIONS=((0, 'NA'), (1, 'EUW'), (2, 'EUNE'), (3, 'BR'))


class Summoner(models.Model):
	region=models.IntegerField(choices=REGIONS, default=0)
	account_id=models.IntegerField(db_index=True)
	summoner_id=models.IntegerField()
	name=models.CharField(max_length=64)
	internal_name=models.CharField(max_length=64)
	level=models.IntegerField()
	profile_icon=models.IntegerField()
	runes=models.TextField(default='', blank=True)
	masteries=models.TextField(default='', blank=True)
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
		return simplejson.loads(self.runes)

	def get_masteries(self):
		return simplejson.loads(self.masteries)

	def get_rating(self):
		try:
			rating=SummonerRating.objects.get(summoner=self, game_map=1, game_mode=3)
		except SummonerRating.DoesNotExist:
			rating=SummonerRating(summoner=self, game_map=1, game_mode=3, wins=0, losses=0, leaves=0, current_rating=0, top_rating=0)
			rating.save()
		return rating

	def _needs_update(self):
		if self.time_updated<(datetime.now(timezone('UTC'))-timedelta(hours=1)):
			updating=cache.get('summoner/{}/{}/updating'.format(self.region, self.account_id))
			if updating!=None:
				return updating
			else:
				return True
		else:
			return False
	needs_update=property(_needs_update)

	def _slug(self):
		return slugify(self.name) if len(slugify(self.name))>0 else '-'
	slug=property(_slug)

	def __unicode__(self):
		return self.name

	class Meta:
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
	game_map=models.IntegerField(choices=MAPS, db_index=True)
	game_mode=models.IntegerField(choices=MODES, db_index=True)
	wins=models.IntegerField()
	losses=models.IntegerField()
	leaves=models.IntegerField()
	current_rating=models.IntegerField(null=True, blank=True)
	top_rating=models.IntegerField(null=True, blank=True)

	class Meta:
		unique_together=(("summoner", "game_map", "game_mode"))


class Game(models.Model):
	region=models.IntegerField(choices=REGIONS, default=0)
	game_id=models.IntegerField()
	game_map=models.IntegerField(choices=MAPS, db_index=True)
	game_mode=models.IntegerField(choices=MODES, db_index=True)
	time=models.DateTimeField()
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
		unique_together=(("region", "game_id"))


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
	sight_wards_bought_in_game=models.IntegerField()
	vision_wards_bought_in_game=models.IntegerField()
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

	def _get_items(self):
		return self.items.split('|')[1:-1]
	get_items=property(_get_items)

	def __unicode__(self):
		return unicode(self.summoner.name)

	class Meta:
		ordering=['game',]
		unique_together=(("game", "summoner"))


def choose_server(region, exclude=None):
	servers=cache.get('servers')
	return servers.choose_server(region)


def check_server(server, region):
	try:
		res=requests.get('{}/{}/'.format(server, 'status'), config={'encode_uri':False}, timeout=20.0)
		if res.json['connected']==True:
			return server
		else:
			print 'switching servers'
			return choose_server(region, [server,])
	except requests.exceptions.Timeout:
		print 'switching servers'
		return choose_server(region, [server,])


def get_data(url, query, region='NA'):
	# server=choose_server(region)
	servers=cache.get('servers')
	server=servers.choose_server(region)
	print 'using server:{}'.format(server)
	try:
		res=requests.get('{}/{}/'.format(server, url), params=query, config={'encode_uri':False}, timeout=20.0)
	except requests.exceptions.Timeout:
		print 'got timeout with:{}'.format(query)
		sleep(5)
		print 'retrying'
		server=servers.check_servers([{'location':server, 'region':region},])
		res=requests.get('{}/{}/'.format(server, url), params=query, config={'encode_uri':False}, timeout=20.0)
	if res.status_code==500:
		print 'got 500 error with:{}'.format(query)
		sleep(5)
		print 'retrying'
		server=servers.check_servers([{'location':server, 'region':region},])
		res=requests.get('{}/{}/'.format(server, url), params=query, config={'encode_uri':False}, timeout=20.0)
	#print res.text
	return res.json


def update_summoners(all_summoners, games=True, runes=False):
	for region in xrange(0,3):
		# if region==1: continue
		summoners=all_summoners.filter(region=region)
		if len(summoners)==0:
			continue
		elif len(summoners)>5:
			print u'running autoupdate for:{}'.format(', '.join(summoners.values_list('name', flat=True)))
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
			print u'running autoupdate for:{}'.format(u', '.join(summoners.values_list('name', flat=True)))
			query={'accounts':u','.join(map(unicode, summoners.values_list('account_id', flat=True))), 'games':1}
			res=get_data('mass_update', query, summoners[0].get_region_display())['accounts']
		for account, data in res.iteritems():
			summoner=Summoner.objects.get(account_id=int(account), region=region)
			summoner=parse_summoner(data['profile'], summoner)
			parse_ratings(data['stats'], summoner)
			if summoner.fully_update:
				parse_games(data['games'], summoner, True)
			else:
				parse_games(data['games'], summoner)
			summoner.time_updated=datetime.now(timezone('UTC'))
			summoner.save()
			cache.delete('{}/{}/updating'.format(summoner.region, summoner.account_id))
			transaction.commit()
	return all_summoners


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
			elif ogame['queue_type'] in ('RANKED_PREMADE_3x3', 'RANKED_PREMADE_5x5'):
				game.game_mode=4
			elif ogame['queue_type'] in ('RANKED_TEAM_3x3', 'RANKED_TEAM_5x5'):
				game.game_mode=5
			elif ogame['queue_type'] in ('NORMAL', 'NORMAL_3x3', 'ODIN_UNRANKED'):
				game.game_mode=2
			elif ogame['queue_type']=='RANKED_SOLO_5x5':
				game.game_mode=3
			elif ogame['queue_type']=='BOT':
				game.game_mode=1
			elif ogame['queue_type']=='NONE' and ogame['game_type']=='CUSTOM_GAME':
				game.game_mode=0
			elif ogame['game_mode']=='ARAM' and ogame['game_type']=='CUSTOM_GAME':
				game.game_mode=6
			elif ogame['game_type']=='TUTORIAL_GAME':
				continue
			else:
				print 'couldn\'t figure out game mode for game #{}'.format(game.game_id)
				print ogame['queue_type']
				print ogame['game_mode']
				print ogame['game_type']
			if ogame['game_map'] in (1, 2, 3, 6):
				game.game_map=1
			elif ogame['game_map']==4:
				game.game_map=0
			elif ogame['game_map']==7:
				game.game_map=3
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
			game.save(force_insert=True)
		if not Player.objects.filter(game=game, summoner=summoner).exists():
			try:
				sr=SummonerRating.objects.get(summoner=summoner, game_map=game.game_map, game_mode=game.game_mode).current_rating
			except SummonerRating.DoesNotExist:
				sr=0
			player=Player(
				game=game,
				summoner=summoner, rating=sr,
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
				minion_kills=ogame['stats']['minions_killed'], neutral_minions_killed=ogame['stats']['neutral_minions_killed'],
				gold=ogame['stats']['gold_earned'],
				damage_dealt=ogame['stats']['damage_dealt'], physical_damage_dealt=ogame['stats']['physical_damage_dealt_player'],	magic_damage_dealt=ogame['stats']['magic_damage_dealt_player'],
				damage_taken=ogame['stats']['damage_taken'], physical_damage_taken=ogame['stats']['physical_damage_taken'], magic_damage_taken=ogame['stats']['magic_damage_taken'],
				total_healing_done=ogame['stats']['total_heal'],
				time_spent_dead=ogame['stats']['total_time_spent_dead'],
				largest_multikill=ogame['stats']['largest_multi_kill'],
				largest_killing_spree=ogame['stats']['largest_killing_spree'],
				largest_critical_strike=ogame['stats']['largest_critical_strike'],
				turrets_destroyed=ogame['stats']['turrets_killed'], inhibitors_destroyed=ogame['stats']['inhibitors_destroyed'],
				sight_wards_bought_in_game=ogame['stats']['sight_wards_bought_in_game'], vision_wards_bought_in_game=ogame['stats']['vision_wards_bought_in_game'],
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
	for game_type, values in GAME_TYPES.iteritems():
		ratings.append(
			SummonerRating(
				summoner=tmp,
				game_mode=values[0],
				game_map=values[1],
				wins=0,
				losses=0,
				leaves=0,
				current_rating=0,
				top_rating=0
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
	# MODES=((0, 'Custom'), (1, 'Bot'), (2, 'Normal'), (3, 'Solo'), (4, 'Premade'), (5, 'Team'), (9, '?'))
	# MAPS=((0, 'Twisted Treeline'), (1, 'Summoners Rift'), (2, 'Dominion'), (9, '?'))
	for rating in SummonerRating.objects.filter(summoner=summoner):
		for r in ratings:
			if r['game_type'] in GAME_TYPES:
				game_mode, game_map=GAME_TYPES[r['game_type']]
			else:
				game_mode, game_map=(9, 9)
			if game_mode==rating.game_mode and game_map==rating.game_map:
				if rating.wins!=int(r['wins']) or rating.losses!=int(r['losses']) or rating.current_rating!=int(r['rating']) or rating.top_rating!=int(r['rating_max']):
					rating.wins=r['wins']
					rating.losses=r['losses']
					rating.current_rating=r['rating']
					rating.top_rating=r['rating_max']
					rating.save(force_update=True)


def parse_masteries(masteries, summoner):
	summoner.masteries=simplejson.dumps(masteries)
	return summoner


def parse_runes(runes, summoner):
	summoner.runes=simplejson.dumps(runes)
	return summoner

from datetime import datetime, timedelta
from django.core.cache import cache
from django.db import models, transaction
from pytz import timezone
from time import sleep
import requests

MAPS=((0, 'Twisted Treeline'), (1, 'Summoners Rift'), (2, 'Dominion'), (9, '?'))
MODES=((0, 'Custom'), (1, 'Bot'), (2, 'Normal'), (3, 'Solo'), (4, 'Premade'), (5, 'Team'), (9, '?'))
GAME_TYPES={'RankedPremade5x5':(4,1), 'RankedTeam5x5':(5,1), 'RankedPremade3x3':(4,0), 'RankedTeam3x3':(5,0), 'Unranked':(2,1), 'OdinUnranked':(2,2), 'RankedSolo5x5':(3,1), 'CoopVsAi':(1,1)}
REGIONS=((0, 'NA'), (1, 'EUW'), (2, 'EUNE'))


class Summoner(models.Model):
	region=models.IntegerField(choices=REGIONS, default=0)
	account_id=models.IntegerField(db_index=True)
	summoner_id=models.IntegerField()
	name=models.CharField(max_length=64)
	internal_name=models.CharField(max_length=64)
	level=models.IntegerField()
	profile_icon=models.IntegerField()
	runes=models.TextField(default='', blank=True)
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
	# players=models.ManyToManyField('Player', related_name='game_players')
	unfetched_players=models.CharField(max_length=128, blank=True)
	fetched=models.BooleanField(default=False)

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
	server=choose_server(region)
	servers=cache.get('servers')
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
			summoner.time_updated=datetime.utcnow().replace(tzinfo=timezone('UTC'))
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
				time=date
			)
			if ogame['game_type']=='PRACTICE_GAME':
				game.game_mode=0
			elif ogame['queue_type'] in ('RANKED_PREMADE_3x3', 'RANKED_PREMADE_5x5'):
				game.game_mode=4
			elif ogame['queue_type'] in ('RANKED_TEAM_3x3', 'RANKED_TEAM_5x5'):
				game.game_mode=5
			elif ogame['queue_type'] in ('NORMAL', 'ODIN_UNRANKED'):
				game.game_mode=2
			elif ogame['queue_type']=='RANKED_SOLO_5x5':
				game.game_mode=3
			elif ogame['queue_type']=='BOT':
				game.game_mode=1
			elif ogame['queue_type']=='NONE' and ogame['game_type']=='CUSTOM_GAME':
				game.game_mode=0
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
			game.save(force_insert=True)
		if not Player.objects.filter(game=game, summoner=summoner).exists():
			try:
				sr=SummonerRating.objects.get(summoner=summoner, game_map=game.game_map, game_mode=game.game_mode).current_rating
			except SummonerRating.DoesNotExist:
				sr=0
			player=Player(
				game=game,
				summoner=summoner,
				rating=sr,
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
			player.save(force_insert=True)
		else:
			player=Player.objects.get(game=game, summoner=summoner)
		# if player not in game.players.all():
		# 	game.players.add(player)
		# 	game.save(force_update=True)
		if not game.fetched and game.time>(datetime.utcnow().replace(tzinfo=timezone('UTC'))-timedelta(days=2)) and full and game!=current:
			print u'Fully updating game:{}'.format(game.game_id)
			print u'For summoner:{}'.format(summoner.name)
			fill_game(game, True)
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

# def fix():
# 	for s in Summoner.objects.all():
# 		GAME_TYPES={'RankedPremade5x5':(4,1), 'RankedTeam5x5':(5,1), 'RankedPremade3x3':(4,0), 'RankedTeam3x3':(5,0), 'Unranked':(2,1), 'OdinUnranked':(2,2), 'RankedSolo5x5':(3,1), 'CoopVsAi':(1,1)}
# 		for game_type, values in GAME_TYPES.iteritems():
# 			if not SummonerRating.objects.filter(summoner=s, game_mode=values[0], game_map=values[1]).exists():
# 				SummonerRating(
# 				summoner=s,
# 				game_map=values[1],
# 				game_mode=values[0],
# 				wins=0,
# 				losses=0,
# 				leaves=0,
# 				current_rating=0,
# 				top_rating=0
# 			).save()


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


@transaction.commit_on_success
def fill_game(game, auto=False):
	if not game.fetched and game.unfetched_players!='':
		names=get_data('get_names', {'ids':game.unfetched_players}, game.get_region_display())
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
				summoner=parse_summoner(data['profile'], summoner)
				parse_ratings(data['stats'], summoner)
			except Summoner.DoesNotExist:
				summoner=create_summoner(data['profile'], game.region)
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
			summoner.save(force_update=True)
		game.fetched=True
		game.save(force_update=True)
	elif not game.fetched and game.unfetched_players=='':
		print 'game was already full'
		game.fetched=True
		game.save(force_update=True)
	return True

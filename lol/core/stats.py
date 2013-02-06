from champions import CHAMPIONS
from lol.models import Player
import json


class Queryset_Manager:
	def __init__(self, queryset, chunksize=5000):
		self.queryset=queryset.order_by('pk')
		self.chunksize=chunksize
		self.count=self.queryset.count()
		if self.count!=0:
			self.pk=self.queryset[0].pk-1
			if self.count>self.chunksize:
				self.last_pk=self.queryset.order_by('-pk')[0].pk

	def __iter__(self):
		if self.count<=self.chunksize:
			for row in self.queryset.filter(pk__gt=self.pk)[:self.chunksize]:
				self.pk=row.pk
				yield row
		else:
			while self.pk<self.last_pk:
				for row in self.queryset.filter(pk__gt=self.pk)[:self.chunksize]:
					self.pk=row.pk
					yield row


class Stats:
		def __init__(self, games, **kwargs):
			self.qs=games.only('game', 'champion_id', 'won', 'items', 'kills', 'deaths', 'assists', 'minion_kills', 'neutral_minions_killed', 'gold', 'summoner_spell1', 'summoner_spell2')
			#.defer(
			# 	'afk', 'leaver', 'blue_team', 'ping', 'queue_length', 'premade_size',
			# 	'ip_earned', 'experience_earned', 'boosted_experience_earned', 'boosted_ip_earned',
			# 	'summoner_level', 'summoner_spell1', 'summoner_spell2',
			# 	'skin_index', 'skin_name',
			# 	'champion_level',
			# 	'summoner__runes', 'summoner__masteries'
			# )
			self.games=Queryset_Manager(self.qs)
			self.indexed=False
			self.items_indexed=False
			self.index={'champions':{}, 'global_stats':{}}
			self.count=0
			self.champion=kwargs.get('champion', None)
			self.summoner_name=kwargs.get('summoner_name', None)
			self.index_items=kwargs.get('index_items', True)
			self.champion_history=kwargs.get('champion_history', False)
			self.index_summoner_spells=kwargs.get('index_summoner_spells', False)
			self.global_stats=kwargs.get('global_stats', False)
			self.display_count=kwargs.get('display_count', self.count)

		def __getstate__(self):
			odict=self.__dict__.copy()
			odict['qs']=self.qs.query
			odict['games']={}
			return odict

		def __setstate__(self, state):
			self.__dict__.update(state)
			self.qs=Player.objects.all()
			self.qs.query=state['qs']
			if not self.indexed or (not self.items_indexed and self.index_items):
				self.games=Queryset_Manager(self.qs)

		def __repr__(self):
			if self.champion!=None:
				return '<Stats for champion {}>'.format(self.champion)
			elif self.summoner_name!=None:
				return '<Stats for {}>'.format(self.summoner_name.encode('utf8', 'replace'))
			else:
				return '<Stats class>'

		def __str__(self):
			if self.champion!=None:
				return '<Stats for champion {}>'.format(self.champion)
			elif self.summoner_name!=None:
				return '<Stats for {}>'.format(self.summoner_name.encode('utf8', 'replace'))
			else:
				return '<Stats class>'

		def __update_count(self):
			if self.display_count==0:
				self.display_count=self.count

		def __index_summoner_spells(self, stats, game):
			for summoner_spell in [game.summoner_spell1, game.summoner_spell2]:
				if summoner_spell not in stats['champions'][game.champion_id]['summoners']:
					stats['champions'][game.champion_id]['summoners'][summoner_spell]={
						'count':	0,
						'won':		0,
						'lost':		0
					}
				stats['champions'][game.champion_id]['summoners'][summoner_spell]['count']+=1
				stats['champions'][game.champion_id]['summoners'][summoner_spell]['won' if game.won else 'lost']+=1
			return stats

		def __index_champion_history(self, stats, game):
			itime=game.game.time.strftime('%Y-%m-%d')
			if game.champion_id not in stats['history'][itime]['champions']:
				stats['history'][itime]['champions'][game.champion_id]={
					'count':	0,
					'won':		0,
					'lost':		0
				}
			stats['history'][itime]['champions'][game.champion_id]['count']+=1
			stats['history'][itime]['champions'][game.champion_id]['won' if game.won else 'lost']+=1
			return stats

		def __index_global_stats(self, stats, game):
			if game.game.game_map==1 and game.game.game_mode!=1:
				stats['global_stats']['blue_side']['won' if game.game.blue_team_won else 'lost']+=1
			return stats

		def __index_items(self, stats, game):
			for item in game.get_items:
				item=int(item)
				if item in (0, 2003, 2004, 2009, 2037, 2038, 2039, 2040, 2042, 2043, 2044, 2047, 2048, 2050): continue
				if item not in stats['champions'][game.champion_id]['items']:
					stats['champions'][game.champion_id]['items'][item]={
						'count':0,
						'won':0,
						'lost':0,
						'kills':0,
						'avg_kills':0,
						'deaths':0,
						'avg_deaths':0
					}
				stats['champions'][game.champion_id]['items'][item]['count']+=1
				stats['champions'][game.champion_id]['items'][item]['kills']+=game.kills
				stats['champions'][game.champion_id]['items'][item]['avg_kills']=round(float(stats['champions'][game.champion_id]['items'][item]['kills'])/stats['champions'][game.champion_id]['items'][item]['count'], 1)
				stats['champions'][game.champion_id]['items'][item]['deaths']+=game.deaths
				stats['champions'][game.champion_id]['items'][item]['avg_deaths']=round(float(stats['champions'][game.champion_id]['items'][item]['deaths'])/stats['champions'][game.champion_id]['items'][item]['count'], 1)
				stats['champions'][game.champion_id]['items'][item]['won' if game.won else 'lost']+=1
			return stats

		def __index(self):
			self.count=self.games.count
			if self.count==0:
				self.indexed=True
				return None
			stats={
				'champions':{},
				'history':{},
				'global_stats':{'blue_side':{'won':0, 'lost':0}}
			}
			for game in self.games:
				if game.champion_id not in stats['champions']:
					stats['champions'][game.champion_id]={
						'count':		0,
						'won':			0,
						'lost':			0,
						'kills':		0,
						'avg_kills':	0,
						'deaths':		0,
						'avg_deaths':	0,
						'kdr':			0,
						'assists':		0,
						'avg_assists':	0,
						'cs':			0,
						'avg_cs':		0,
						'gold':			0,
						'avg_gold':		0,
						'items':		{},
						'summoners':	{}
					}
				stats['champions'][game.champion_id]['count']+=1
				for key, mapping in {'kills':'kills', 'deaths':'deaths', 'assists':'assists', 'minion_kills':'cs', 'neutral_minions_killed':'cs', 'gold':'gold'}.iteritems():
					stats['champions'][game.champion_id][mapping]+=getattr(game, key)
					stats['champions'][game.champion_id]['avg_{}'.format(mapping)]=round(float(stats['champions'][game.champion_id][mapping])/stats['champions'][game.champion_id]['count'], 1)
				if stats['champions'][game.champion_id]['deaths']>0:
					stats['champions'][game.champion_id]['kdr']=round(float(stats['champions'][game.champion_id]['kills'])/stats['champions'][game.champion_id]['deaths'], 2)
				else:
					stats['champions'][game.champion_id]['kdr']=round(float(stats['champions'][game.champion_id]['kills']), 2)
				stats['champions'][game.champion_id]['won' if game.won else 'lost']+=1

				if self.index_items:
					stats=self.__index_items(stats, game)
				if self.champion_history:
					itime=game.game.time.strftime('%Y-%m-%d')
					if itime not in stats['history']:
						stats['history'][itime]={
							'count':	0,
							'champions':{}
						}
					stats['history'][itime]['count']+=1
					stats=self.__index_champion_history(stats, game)
				if self.index_summoner_spells:
					stats=self.__index_summoner_spells(stats, game)
				if self.global_stats:
					stats=self.__index_global_stats(stats, game)
			# self.index={'champions':champions, 'elo':sorted(elo.iteritems(), key=lambda x:x[0]), 'history':sorted(history.iteritems(), key=lambda x:x[0])[:-1], 'global_stats':global_stats}
			stats['history']=sorted(stats['history'].iteritems(), key=lambda x:x[0])[:-1]
			self.index=stats
			self.indexed=True
			if self.index_items: self.items_indexed=True
			self.__update_count()
			# self.games=Queryset_Manager(self.qs)

		def __champions(self):
			if not self.indexed: self.__index()
			return self.index['champions']
		champions=property(__champions)

		def generate_index(self):
			if not self.indexed: self.__index()
			return True

		def by_name(self):
			def __get_name(c):
				return CHAMPIONS[c[0]]
			if not self.indexed: self.__index()
			return sorted(self.index['champions'].iteritems(), key=__get_name)

		def by_count(self):
			if not self.indexed: self.__index()
			return sorted(self.index['champions'].iteritems(), key=lambda g:g[1]['count'], reverse=True)

		def best_ratio(self, minimum=None):
			def bsort(g):
				if g[1]['count']>=minimum:
					return g[1]['won']-g[1]['lost']
				else:
					return -100
			if not self.indexed: self.__index()
			if minimum==None:
				minimum=round(self.count*0.04)
			return sorted(self.index['champions'].iteritems(), key=bsort, reverse=True)

		def items_most_used(self, champion_id=None):
			if not self.items_indexed: self.__index()
			if champion_id==None: champion_id=self.champion
			return sorted(self.index['champions'][champion_id]['items'].iteritems(), key=lambda g:g[1]['count'], reverse=True)

		def items_best_ratio(self, champion_id=None, minimum=None):
			def bsort(g):
				if g[1]['count']>=minimum:
					return g[1]['won']-g[1]['lost']
				else:
					return -100
			if not self.items_indexed: self.__index()
			if champion_id==None: champion_id=self.champion
			if minimum==None:
				minimum=round(self.index['champions'][champion_id]['count']*0.05)
			return sorted(self.index['champions'][champion_id]['items'].iteritems(), key=bsort, reverse=True)

		def elo_toJSON(self):
			return json.dumps(self.index['elo'])

		def history_toJSON(self):
			return json.dumps(self.index['history'])

from champions import CHAMPIONS
from lol.models import Player
import simplejson


class queryset_manager:
	def __init__(self, queryset, chunksize=5000):
		self.queryset=queryset.order_by('pk')
		self.count=self.queryset.count()
		if self.count!=0:
			self.last_pk=self.queryset.order_by('-pk')[0].pk
			self.pk=self.queryset[0].pk - 1
		self.chunksize=chunksize

	def __iter__(self):
		while self.pk<self.last_pk:
			for row in self.queryset.filter(pk__gt=self.pk)[:self.chunksize]:
				self.pk=row.pk
				yield row


class Stats:
		def __init__(self, games, **kwargs):
			self.qs=games
			self.games=queryset_manager(self.qs)
			self.indexed=False
			self.items_indexed=False
			self.index={'champions':{}, 'elo':{}}
			self.count=0
			self.champion=kwargs.get('champion', None)
			self.summoner_name=kwargs.get('summoner_name', None)
			self.cached=kwargs.get('cached', False)
			self.index_elo=kwargs.get('elo', False)
			self.champion_history=kwargs.get('champion_history', False)
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
			self.games=queryset_manager(self.qs)

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

		def __index(self):
			self.count=self.games.count
			if self.count==0:
				self.indexed=True
				return None
			champions={}
			history={}
			elo={}
			for game in self.games:
				itime=game.game.time.strftime('%Y-%m-%d')
				if itime not in history:
					history[itime]={
						'count':	0,
						'champions':{}
					}
				history[itime]['count']+=1
				if self.index_elo and self.summoner_name!=None and game.game.game_map==1 and game.game.game_mode==3 and game.rating!=0:
					if itime not in elo:
						elo[itime]={
							'count':	0,
							'total':	0,
							'rating':	0
						}
					elo[itime]['count']+=1
					#  use avg elo for day
					elo[itime]['total']+=float(game.rating)
					elo[itime]['rating']=int(elo[itime]['total']/elo[itime]['count'])
					#  use max elo for day
					# if game.rating>elo[itime]['rating']:
					# 	elo[itime]['rating']=game.rating
				if self.champion_history:
					if game.champion_id not in history[itime]['champions']:
						history[itime]['champions'][game.champion_id]={
							'count':	0,
							'won':		0,
							'lost':		0
						}
					history[itime]['champions'][game.champion_id]['count']+=1
					history[itime]['champions'][game.champion_id]['won' if game.won else 'lost']+=1
				if game.champion_id not in champions:
					champions[game.champion_id]={
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
						'items':		{}
					}
				champions[game.champion_id]['count']+=1
				champions[game.champion_id]['kills']+=game.kills
				champions[game.champion_id]['avg_kills']=round(float(champions[game.champion_id]['kills'])/champions[game.champion_id]['count'], 1)
				champions[game.champion_id]['deaths']+=game.deaths
				champions[game.champion_id]['avg_deaths']=round(float(champions[game.champion_id]['deaths'])/champions[game.champion_id]['count'], 1)
				champions[game.champion_id]['assists']+=game.assists
				champions[game.champion_id]['avg_assists']=round(float(champions[game.champion_id]['assists'])/champions[game.champion_id]['count'], 1)
				champions[game.champion_id]['cs']+=game.minion_kills+game.neutral_minions_killed
				champions[game.champion_id]['avg_cs']=champions[game.champion_id]['cs']/champions[game.champion_id]['count']
				champions[game.champion_id]['gold']+=game.gold
				champions[game.champion_id]['avg_gold']=champions[game.champion_id]['gold']/champions[game.champion_id]['count']
				if champions[game.champion_id]['deaths']>0:
					champions[game.champion_id]['kdr']=round(float(champions[game.champion_id]['kills'])/champions[game.champion_id]['deaths'], 2)
				else:
					champions[game.champion_id]['kdr']=round(float(champions[game.champion_id]['kills']), 2)
				champions[game.champion_id]['won' if game.won else 'lost']+=1
			self.index={'champions':champions, 'elo':sorted(elo.iteritems(), key=lambda x:x[0]), 'history':sorted(history.iteritems(), key=lambda x:x[0])[:-1]}
			self.indexed=True
			self.__update_count()
			self.games=queryset_manager(self.qs)

		def __index_items(self):
			if not self.indexed: self.__index()
			if self.count==0:
				self.items_indexed=True
				return None
			for game in self.games:
				for item in game.get_items:
					item=int(item)
					if item==0: continue
					if item not in self.index['champions'][game.champion_id]['items']:
						self.index['champions'][game.champion_id]['items'][item]={
							'count':0,
							'won':0,
							'lost':0,
							'kills':0,
							'avg_kills':0,
							'deaths':0,
							'avg_deaths':0
						}
					self.index['champions'][game.champion_id]['items'][item]['count']+=1
					self.index['champions'][game.champion_id]['items'][item]['kills']+=game.kills
					self.index['champions'][game.champion_id]['items'][item]['avg_kills']=round(float(self.index['champions'][game.champion_id]['items'][item]['kills'])/self.index['champions'][game.champion_id]['items'][item]['count'], 1)
					self.index['champions'][game.champion_id]['items'][item]['deaths']+=game.deaths
					self.index['champions'][game.champion_id]['items'][item]['avg_deaths']=round(float(self.index['champions'][game.champion_id]['items'][item]['deaths'])/self.index['champions'][game.champion_id]['items'][item]['count'], 1)
					self.index['champions'][game.champion_id]['items'][item]['won' if game.won else 'lost']+=1
			self.items_indexed=True
			self.__update_count()
			# self.games=queryset_manager(self.qs)

		def __champions(self):
			if not self.indexed: self.__index()
			return self.index['champions']
		champions=property(__champions)

		def generate_index(self, items=False):
			if not items:
				if not self.indexed: self.__index()
			else:
				if not self.items_indexed: self.__index_items()
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
			if not self.items_indexed: self.__index_items()
			if champion_id==None: champion_id=self.champion
			return sorted(self.index['champions'][champion_id]['items'].iteritems(), key=lambda g:g[1]['count'], reverse=True)

		def items_best_ratio(self, champion_id=None, minimum=None):
			def bsort(g):
				if g[1]['count']>=minimum:
					return g[1]['won']-g[1]['lost']
				else:
					return -100
			if not self.items_indexed: self.__index_items()
			if champion_id==None: champion_id=self.champion
			if minimum==None:
				minimum=round(self.index['champions'][champion_id]['count']*0.05)
			return sorted(self.index['champions'][champion_id]['items'].iteritems(), key=bsort, reverse=True)

		def elo_toJSON(self):
			return simplejson.dumps(self.index['elo'])

		def history_toJSON(self):
			return simplejson.dumps(self.index['history'])

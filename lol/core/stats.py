from champions import CHAMPIONS


class queryset_manager:
	def __init__(self, queryset, chunksize=2000):
		self.queryset=queryset.order_by('pk')
		self.last_pk=queryset.order_by('-pk')[0].pk
		self.chunksize=chunksize
		self.pk=self.queryset[0].pk - 1

	def __iter__(self):
		while self.pk<self.last_pk:
			for row in self.queryset.filter(pk__gt=self.pk)[:self.chunksize]:
				self.pk=row.pk
				yield row


class Stats(object):
		def __init__(self, games, champion=None, summoner_name=None):
			self.qs=games
			self.games=queryset_manager(self.qs)
			self.indexed=False
			self.items_indexed=False
			self.index={}
			self.count=0
			if champion!=None:
				self.champion=int(champion)
			else:
				self.champion=None
			self.summoner_name=summoner_name

		def __str__(self):
			if self.champion!=None:
				return '<Stats for champion {}>'.format(self.champion)
			elif self.summoner_name!=None:
				return '<Stats for {}>'.format(self.summoner_name)
			else:
				return '<Stats class>'

		def __index(self):
			self.count=self.qs.count()
			champions={}
			for game in self.games:
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
				if game.won:
					champions[game.champion_id]['won']+=1
				else:
					champions[game.champion_id]['lost']+=1
			self.index={'champions':champions}
			self.indexed=True
			self.games=queryset_manager(self.qs)

		def __index_items(self):
			if not self.indexed: self.__index()
			for game in self.games:
				for item in game.get_items:
					item=int(item)
					if item==0: continue
					if item not in self.index['champions'][game.champion_id]['items']:
						self.index['champions'][game.champion_id]['items'][item]={
							'count':0,
							'won':0,
							'lost':0
						}
					self.index['champions'][game.champion_id]['items'][item]['count']+=1
					if game.won:
						self.index['champions'][game.champion_id]['items'][item]['won']+=1
					else:
						self.index['champions'][game.champion_id]['items'][item]['lost']+=1
			self.items_indexed=True
			self.games=queryset_manager(self.qs)

		def __champions(self):
			if not self.indexed: self.__index()
			return self.index['champions']
		champions=property(__champions)

		def generate_index(self):
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

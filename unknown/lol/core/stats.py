from champions import CHAMPIONS


class Stats(object):
		def __init__(self, games, champion=None):
			self.games=games
			self.indexed=False
			self.items_indexed=False
			self.index={}
			self.count=0
			if champion!=None:
				self.champion=int(champion)
			else:
				self.champion=None

		def __index(self):
			self.count=len(self.games)
			items={}
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
				champions[game.champion_id]['avg_kills']=champions[game.champion_id]['kills']/champions[game.champion_id]['count']
				champions[game.champion_id]['deaths']+=game.deaths
				champions[game.champion_id]['avg_deaths']=champions[game.champion_id]['deaths']/champions[game.champion_id]['count']
				champions[game.champion_id]['assists']+=game.assists
				champions[game.champion_id]['avg_assists']=champions[game.champion_id]['assists']/champions[game.champion_id]['count']
				champions[game.champion_id]['cs']+=game.minion_kills+game.neutral_minions_killed
				champions[game.champion_id]['avg_cs']=champions[game.champion_id]['cs']/champions[game.champion_id]['count']
				champions[game.champion_id]['gold']+=game.gold
				champions[game.champion_id]['avg_gold']=champions[game.champion_id]['gold']/champions[game.champion_id]['count']
				if game.won:
					champions[game.champion_id]['won']+=1
				else:
					champions[game.champion_id]['lost']+=1
				# itt=game.get_items
				# for i in itt:
				# 	i=int(i)
				# 	if i==0:
				# 		continue
				# 	if i not in items:
				# 		items[i]={'count':0, 'won':0, 'lost':0}
				# 	items[i]['count']+=1
				# 	if game.won:
				# 		items[i]['won']+=1
				# 	else:
				# 		items[i]['lost']+=1
			self.index={'champions':champions, 'items':items}
			self.indexed=True

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

		def __champions(self):
			if not self.indexed: self.__index()
			return self.index['champions']
		champions=property(__champions)

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
				minimum=round(self.count*0.05)
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

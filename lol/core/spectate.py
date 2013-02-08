from lol.core.champions import CHAMPIONS
from django.core.cache import cache
# from models import Summoner


class Spectate:
	def __init__(self, name):
		self.name=name
		self.status=0
		self.timeout=300
		self.info={}

	def __str__(self):
		if self.status!=2:
			return {-1:'Not in a game.', -2:'Game not observable.', 0:'?', 1:'Game not started.'}[self.status]
		else:
			return self.link

	def parse(self, data):
		if 'error' in data:
			self.status={'OB-1':-1, 'OB-2':-2, 'OB-3':1}[data['error']]
			if self.status==0:
				pass
		else:
			self.status=2
			self.info=data

	def player_info(self, region, account_id):
		if self.status!=2: return ''
		# summoner=Summoner.objects.get(account_id=account_id, region=region)
		index=[i for i,x in enumerate(self.info['info']['players']) if x['account_id']==account_id][0]
		player=self.info['info']['players'][index]
		return 'Currently playing as {}.'.format(CHAMPIONS[player['champion']])

	def save(self):
		cache.set(self.name, self, self.timeout)

	def _url(self):
		return "lolspectate://ip={ip}&port={port}&game_id={game_id}&region={region}&key={key}".format(**self.info)
		#return "lrf://spectator {ip} {key} {game_id} {region} 1.0.0.152"
	url=property(_url)

	def _link(self):
		return "<a href='{}'>Spectate game.</a>".format(self.url)
	link=property(_link)

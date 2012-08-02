from django.core.cache import cache


class Spectate:
	def __init__(self, task, name):
		self.task=task
		self.name=name
		self.status=0
		self.timeout=300
		self.info={}

	def __str__(self):
		if self.status!=2:
			return {-1:'Not in a game.', -2:'Game not observable.', 0:'?', 1:'Game not started.'}[self.status]
		else:
			return self.link()

	def check(self):
		if self.status>=0:
			if self.task.ready():
				self.parse(self.task.result)
				self.save()

	def parse(self, info):
		if 'error' in info:
			self.status={'OB-1':-1, 'OB-2':-2, 'OB-3':1}[info['error']]
			if self.status==0:
				pass
		else:
			self.status=2
			self.info=info

	def save(self):
		cache.set(self.name, self, self.timeout)

	def link(self):
		return "<a href='lolspectate://ip={ip}&port={port}&game_id={game_id}&region={region}&key={key}'>Spectate game.</a>".format(**self.info)

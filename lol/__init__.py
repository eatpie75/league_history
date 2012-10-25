import requests
import random
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
from redis.exceptions import ConnectionError


class NoServersAvailable(Exception):
	pass


class Server_List:
	"""
	Statuses:{-1:Unknown, 0:Down, 1:Up}
	"""
	def __init__(self, server_list):
		self.updated=None
		self.servers={}
		for region, data in server_list.iteritems():
			self.servers[region]={}
			for server in data:
				self.servers[region][server]=-1
		self.check_servers()

	def check_servers(self, server=None, **kwargs):
		def __check(server):
			try:
				res=requests.get('{}/{}/'.format(server, 'status'), config={'encode_uri':False}, timeout=20.0)
				if res.status_code==200 and res.json['connected']==True:
					return 1
				else:
					return 0
			except:
				return 0
		if server==None:
			for region, data in self.servers.iteritems():
				for server, status in data.iteritems():
					if (kwargs.get('up', True)==False and status==1) or (kwargs.get('down', True)==False and status==0) or (kwargs.get('unknown', True)==False and status==-1):
						continue
					self.servers[region][server]=__check(server)
			self.updated=datetime.now()
			cache.set('servers', self, timeout=0)
		else:
			for s in server:
				region=s['region']
				location=s['location']
				self.servers[region][location]=__check(location)
				cache.set('servers', self, timeout=0)
			return self.choose_server(region)

	def __filter_up(self, region):
		return filter(lambda data:True if self.servers[region][data]==1 else False, self.servers[region])

	def __filter_down(self, region):
		return filter(lambda data:True if self.servers[region][data]==0 else False, self.servers[region])

	def choose_server(self, region):
		choices=self.__filter_up(region)
		if len(choices)==0:
			raise NoServersAvailable()
		else:
			return random.choice(choices)

try:
	servers=cache.get('servers')
	if servers==None:
		sl=Server_List(settings.LOL_CLIENT_SERVERS)
		cache.set('servers', sl, timeout=0)
	else:
		if servers.updated<datetime.now()-timedelta(hours=1):
			servers.check_servers()
	if cache.get('queue_len')==None:
		cache.set('queue_len', 0, timeout=0)
except ConnectionError:
	print 'Couldn\'t connect to redis, lots of things will be broken'

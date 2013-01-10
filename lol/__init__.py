from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
from pytz import timezone
from redis.exceptions import ConnectionError
import requests
import random


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
			self.servers[region]=[]
			for server in data:
				self.servers[region].append({'url':server, 'status':-1, 'last_updated':None})
		self.check_servers()

	def check_servers(self, server=None, **kwargs):
		def __check(server):
			try:
				res=requests.get('{}/{}/'.format(server, 'status'), timeout=20.0)
				if res.status_code==200 and res.json()['connected']==True:
					return 1
				else:
					return 0
			except:
				return 0
		if server==None:
			for region, data in self.servers.iteritems():
				i=-1
				for server in data:
					i+=1
					if (kwargs.get('up', True)==False and server['status']==1) or (kwargs.get('down', True)==False and server['status']==0) or (kwargs.get('unknown', True)==False and server['status']==-1):
						continue
					self.servers[region][i]['status']=__check(server['url'])
					self.servers[region][i]['last_updated']=datetime.now(timezone('UTC'))
			self.updated=datetime.now(timezone('UTC'))
			cache.set('servers', self, timeout=0)
		else:
			for s in server:
				region=s['region']
				url=s['url']
				index=[i for i,x in enumerate(self.servers[region]) if x['url']==url][0]
				self.servers[region][index]['status']=__check(url)
				cache.set('servers', self, timeout=0)
			return self.choose_server(region)

	def __filter_up(self, region):
		return filter(lambda data:True if data['status']==1 else False, self.servers[region])

	def __filter_down(self, region):
		return filter(lambda data:True if data['status']==0 else False, self.servers[region])

	def __available_regions(self):
		pass

	def choose_server(self, region):
		choices=self.__filter_up(region)
		if len(choices)==0:
			raise NoServersAvailable()
		else:
			return random.choice(choices)['url']

try:
	servers=cache.get('servers')
	if servers==None:
		sl=Server_List(settings.LOL_CLIENT_SERVERS)
		cache.set('servers', sl, timeout=0)
	else:
		if servers.updated<datetime.now(timezone('UTC'))-timedelta(hours=1):
			servers.check_servers()
	if cache.get('queue_len')==None:
		cache.set('queue_len', 0, timeout=0)
except ConnectionError:
	print 'Couldn\'t connect to redis, lots of things will be broken'

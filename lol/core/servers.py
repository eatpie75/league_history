from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
from pytz import timezone
from redis_cache.exceptions import ConnectionInterrupted
import requests
import random

REGIONS=((0, 'NA'), (1, 'EUW'), (2, 'EUNE'), (3, 'BR'))
SUPPORTED_REGIONS=('NA', 'EUW', 'EUNE')


class NoServersAvailable(Exception):
	pass


class Server_List:
	"""
	Statuses:{-1:Unknown, 0:Down, 1:Up}
	"""
	def __init__(self, server_list):
		self.updated=None
		self.servers={}
		for region in SUPPORTED_REGIONS:
			self.servers[region]=[]
		for region, data in server_list.iteritems():
			for server in data:
				self.servers[region].append({'url':server, 'status':-1, 'last_updated':None, 'metadata':{}})
		self.check_servers()

	def __filter_up(self, region):
		return filter(lambda data:True if data['status']==1 else False, self.servers[region])

	def __filter_down(self, region):
		return filter(lambda data:True if data['status']==0 else False, self.servers[region])

	def find_by_url(self, region, url):
		return [i for i,x in enumerate(self.servers[region]) if x['url']==url][0]

	def __available_regions(self):
		available=[]
		for region, data in self.servers.iteritems():
			for server in data:
				if server['status']==1 and region not in available:
					available.append(region)
		return available
	available_regions=property(__available_regions)

	def set_metadata(self, region, url, data, save=True):
		index=self.find_by_url(region, url)
		for prop, val in data.iteritems():
			self.servers[region][index]['metadata'][prop]=val
		if save: self.save()

	def check_servers(self, server=None, **kwargs):
		def __check(server):
			try:
				res=requests.get('{}/{}/'.format(server, 'status'), timeout=20.0)
				if res.status_code==200 and res.json()['data']['connected'] is True:
					return 1
				else:
					return 0
			except:
				return 0
		if server is None:
			for region, data in self.servers.iteritems():
				i=-1
				for server in data:
					i+=1
					if (kwargs.get('up', True) is False and server['status']==1) or (kwargs.get('down', True) is False and server['status']==0) or (kwargs.get('unknown', True) is False and server['status']==-1):
						continue
					self.servers[region][i]['status']=__check(server['url'])
					self.servers[region][i]['last_updated']=datetime.now(timezone('UTC'))
			self.updated=datetime.now(timezone('UTC'))
			self.save()
		else:
			for s in server:
				region=s['region']
				url=s['url']
				index=self.find_by_url(region, url)
				self.servers[region][index]['status']=__check(url)
				self.save()
			return self.choose_server(region)

	def choose_server(self, region):
		choices=self.__filter_up(region)
		if len(choices)==0:
			raise NoServersAvailable()
		else:
			return random.choice(choices)

	def save(self):
		cache.set('servers', self, timeout=0)


def prepare_servers():
	print('running server prep')
	try:
		servers=cache.get('servers')
		if servers is None:
			sl=Server_List(settings.LOL_CLIENT_SERVERS)
			sl.save()
		else:
			if servers.updated<datetime.now(timezone('UTC')) - timedelta(hours=1):
				servers.check_servers()
		if cache.get('event_list') is None:
			cache.set('event_list', [], timeout=0)
	except ConnectionInterrupted:
		print 'Couldn\'t connect to redis, lots of things will be broken'
	return True

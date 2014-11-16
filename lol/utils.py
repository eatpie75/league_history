from django.core.cache import cache
from django.core.urlresolvers import reverse
from lol.core.servers import REGIONS
import re


def log_event(level, time, text, data={}):
	event_list=cache.get('event_list')
	if event_list is None:
		event_list=[]
	if len(event_list)>=25:
		del event_list[0:len(event_list) - 24]
	event_list.append((level, time, text, data))
	cache.set('event_list', event_list)
	return True


class EventList(object):
	def __init__(self, event_list):
		if event_list is None:
			event_list=[]
		self.raw_event_list=event_list[::-1]
		self.event_list=[]
		self.parse()

	def parse(self):
		for event in self.raw_event_list:
			event_text=event[2]
			data=event[3]
			nevent=[event[0], event[1]]
			if len(data)>0:
				event_type=data['type']
				if event_type=='summoner':
					region=REGIONS[data['summoner']['region']][1]
					url=reverse('view_summoner_redirect', kwargs={'region':region, 'account_id':data['summoner']['account_id']})
					url=u": <a href='{}'>{}</a>".format(url, data['summoner']['name'])
					nevent.append(re.sub(ur':.*?$', url, event_text, flags=re.IGNORECASE | re.DOTALL | re.UNICODE))
					self.event_list.append(tuple(nevent))
				elif event_type=='game':
					region=REGIONS[data['game']['region']][1]
					url=reverse('view_game', kwargs={'region':region, 'game_id':data['game']['game_id']})
					url=u": <a href='{}'>{}/{}</a>".format(url, region, data['game']['game_id'])
					nevent.append(re.sub(ur':.*?$', url, event_text, flags=re.IGNORECASE | re.DOTALL | re.UNICODE))
					self.event_list.append(tuple(nevent))
			else:
				nevent.append(event_text)
				self.event_list.append(tuple(nevent))
		return self.event_list

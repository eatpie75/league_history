from django.core.cache import cache


def log_event(level, time, name, text):
	event_list=cache.get('event_list')
	if event_list is None:
		event_list=[]
	if len(event_list)>=25:
		del event_list[0:len(event_list) - 24]
	event_list.append((level, time, name, text))
	cache.set('event_list', event_list)
	return True

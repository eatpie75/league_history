from celery.task import task
from datetime import datetime, timedelta
from django.core.cache import cache
from django.db import transaction
from lol.models import Summoner, update_summoners, get_data, parse_games, parse_ratings, parse_summoner
from pytz import timezone


@task
def auto_update():
	update_summoners(Summoner.objects.filter(update_automatically=True, time_updated__lt=(datetime.utcnow().replace(tzinfo=timezone('UTC'))-timedelta(hours=3))))


@task(track_started=True)
def background_update(summoner):
	update_summoners(summoner)
	print 'finished'


@task(ignore_result=True)
def check_servers(**kwargs):
	server_list=cache.get('servers')
	server_list.check_servers(up=kwargs.get('up', True), down=kwargs.get('down', True), unknown=kwargs.get('unknown', True))


@task
@transaction.commit_on_success
def summoner_auto(summoner):
	print u'running autoupdate for:{}'.format(summoner.name)
	query={'accounts':summoner.account_id,'games':1}
	data=get_data('mass_update', query, summoner.get_region_display())['accounts'][str(summoner.account_id)]
	summoner=parse_summoner(data['profile'], summoner)
	parse_ratings(data['stats'], summoner)
	if summoner.fully_update:
		parse_games(data['games'], summoner, True)
	else:
		parse_games(data['games'], summoner)
	summoner.time_updated=datetime.utcnow().replace(tzinfo=timezone('UTC'))
	summoner.save()
	cache.delete('{}/{}/updating'.format(summoner.region, summoner.account_id))
	cache.delete('{}/{}/stats'.format(summoner.region, summoner.account_id))
	print u'finished autoupdate for:{}'.format(summoner.name)
	return summoner

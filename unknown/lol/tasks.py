from celery.task import task
from datetime import datetime, timedelta
from models import Summoner, update_summoners, fill_game
from pytz import timezone


@task
def up(summoner):
	update_summoners(summoner)
	return True


@task
def auto():
	update_summoners(Summoner.objects.filter(update_automatically=True, time_updated__lt=(datetime.utcnow().replace(tzinfo=timezone('UTC'))-timedelta(hours=1))))
	return True


@task
def fg(game):
	fill_game(game)
	return True

from datetime import datetime, timedelta
from django.core.management.base import NoArgsCommand
from lol.models import Summoner, Player, update_summoners, fill_game
from pytz import timezone


class Command(NoArgsCommand):

	def handle_noargs(self, **options):
		summoners=Summoner.objects.filter(update_automatically=True, time_updated__lt=(datetime.utcnow().replace(tzinfo=timezone('UTC'))-timedelta(hours=3)))
		self.stdout.write('updating {} summoners\n'.format(len(summoners)))
		update_summoners(summoners)
		games=Player.objects.filter(summoner__update_automatically=True, game__fetched=False, game__time__gt=(datetime.utcnow().replace(tzinfo=timezone('UTC'))-timedelta(days=2)))
		for player in games:
			fill_game(player.game)
		raw_input('...')

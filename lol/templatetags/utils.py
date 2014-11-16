from datetime import datetime
from django_jinja import library
from lol.models import TIERS, DIVISIONS
from pytz import timezone


@library.filter
def get_percent(val1, val2):
	return '{:.0%}'.format(float(val1) / float(val2)) if val2!=0 else '0%'


@library.filter
def to_k_format(value):
	try:
		value=int(value)
	except (TypeError, ValueError):
		return value
	if value<1000:
		return value
	tmp='{:.1f}K'.format(value / 1000.0)
	if tmp.count('.0K'):
		tmp=tmp.replace('.0', '')
	return tmp


@library.filter
def is_in_game(player, game):
	if player.game_id==game.pk:
		return True
	else:
		return False


@library.filter
def timediff(val1, val2=None):
	if val2 is None:
		val2=datetime.now(timezone('UTC'))
	diff=val2 - val1
	return diff.total_seconds()


@library.filter
def number_to_rank(number):
	tier=number // 500 + 1
	division=(number - (tier - 1) * 500) // 100
	rank=100 - (number - (tier - 1) * 500 - division * 100)
	if tier==6:
		division=4
	return {'tier':int(tier), 'division':int(5 - division), 'rank':int(rank)}


@library.filter
def display_rank(rank):
	tier=next(name for value, name in TIERS if value==rank['tier'])
	division=next(name for value, name in DIVISIONS if value==rank['division'])
	if rank['tier']==6:
		return tier
	else:
		return '{}:{}'.format(tier, division)

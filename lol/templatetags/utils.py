from coffin import template
from datetime import datetime
from lol.models import TIERS, DIVISIONS
from pytz import timezone

register = template.Library()


@register.filter
def get_percent(val1, val2):
	return '{:.0%}'.format(float(val1)/float(val2))


@register.filter
def to_k_format(value):
	try:
		value=int(value)
	except (TypeError, ValueError):
		return value
	if value<1000:
		return value
	tmp='{:.1f}K'.format(value/1000.0)
	if tmp.count('.0K'):
		tmp=tmp.replace('.0', '')
	return tmp


@register.filter
def is_in_game(player, game):
	if player.game_id==game.pk:
		return True
	else:
		return False


@register.filter
def timediff(val1, val2=None):
	if val2 is None:
		val2=datetime.now(timezone('UTC'))
	diff=val2-val1
	return diff.total_seconds()


@register.filter
def number_to_rank(number):
	tier=number//500+1
	division=(number-(tier-1)*500)//100
	rank=100-(number-(tier-1)*500-division*100)
	if tier==6: division=4
	return {'tier':int(tier), 'division':int(5-division), 'rank':int(rank)}


@register.filter
def display_rank(rank):
	print(rank)
	tier=next(name for value, name in TIERS if value==rank['tier'])
	division=next(name for value, name in DIVISIONS if value==rank['division'])
	if rank['tier']==6:
		return tier
	else:
		return '{}:{}'.format(tier, division)

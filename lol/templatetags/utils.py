from coffin import template
from datetime import datetime
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
def timediff(val1, val2=datetime.now(timezone('UTC'))):
	return (val2-val1).total_seconds()

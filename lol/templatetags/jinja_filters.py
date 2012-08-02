from datetime import date, datetime
from django.template import defaultfilters
from django.utils.translation import pgettext, ungettext, ugettext as _
from django.utils.timezone import is_aware, utc
from coffin import template
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


@register.filter
def naturaltime(value):
	"""
	For date and time values shows how many seconds, minutes or hours ago
	compared to current timestamp returns representing string.
	"""
	if not isinstance(value, date):  # datetime is a subclass of date
		return value

	now = datetime.now(utc if is_aware(value) else None)
	if value < now:
		delta = now - value
		if delta.days != 0:
			return pgettext(
				'naturaltime', '%(delta)s ago'
				) % {'delta': defaultfilters.timesince(value)}
		elif delta.seconds == 0:
			return _('now')
		elif delta.seconds < 60:
			return ungettext(
				'a second ago', '%(count)s seconds ago', delta.seconds
				) % {'count': delta.seconds}
		elif delta.seconds // 60 < 60:
			count = delta.seconds // 60
			return ungettext(
				'a minute ago', '%(count)s minutes ago', count
				) % {'count': count}
		else:
			count = delta.seconds // 60 // 60
			return ungettext(
				'an hour ago', '%(count)s hours ago', count
				) % {'count': count}
	else:
		delta = value - now
		if delta.days != 0:
			return pgettext(
				'naturaltime', '%(delta)s from now'
				) % {'delta': defaultfilters.timeuntil(value)}
		elif delta.seconds == 0:
			return _('now')
		elif delta.seconds < 60:
			return ungettext(
				'a second from now', '%(count)s seconds from now', delta.seconds
				) % {'count': delta.seconds}
		elif delta.seconds // 60 < 60:
			count = delta.seconds // 60
			return ungettext(
				'a minute from now', '%(count)s minutes from now', count
				) % {'count': count}
		else:
			count = delta.seconds // 60 // 60
			return ungettext(
				'an hour from now', '%(count)s hours from now', count
				) % {'count': count}

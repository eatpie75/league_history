from django import template

register = template.Library()


def get_percent(val1, val2):
	return '{:.0%}'.format(float(val1)/float(val2))

register.filter('get_percent', get_percent)

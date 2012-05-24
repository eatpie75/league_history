from django import template

register = template.Library()


@register.filter(is_safe=False)
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

register.filter('to_k_format', to_k_format)

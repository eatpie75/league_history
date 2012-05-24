from django import template

register = template.Library()


def get_key(obj, key):
	return obj.get(key)

register.filter('get_key', get_key)

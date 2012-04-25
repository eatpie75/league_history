from django import template

register = template.Library()

def get_key(a, b):
	from pprint import pprint
	return a.get(b)

register.filter('get_key', get_key)
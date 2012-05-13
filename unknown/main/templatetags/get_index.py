from django import template

register = template.Library()


def get_index(obj, index):
	return obj[index]

register.filter('get_index', get_index)

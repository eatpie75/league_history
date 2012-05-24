#from django.core import serializers
from django.http import HttpResponse
from django.utils import simplejson
from models import Game, Player


def player_info(request, player):
	player=Player.objects.filter(pk=player)
	return HttpResponse(simplejson.dumps(list(player.values())[0]), mimetype='application/json')

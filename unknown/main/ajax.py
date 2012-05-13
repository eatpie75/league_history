#from django.core import serializers
from django.http import HttpResponse
from django.utils import simplejson
from models import Game
from unknown.rcimport.models import Game as IGame, Player as IPlayer, RunePage, RuneSlot, Summoner as ISummoner, SummonerRankedStatistics, SummonerRating as ISummonerRating, Team as Iteam, UnknownPlayer as IUnknownPlayer


def player_info(request, player):
	player=IPlayer.objects.filter(pk=player)
	return HttpResponse(simplejson.dumps(list(player.values())[0]), mimetype='application/json')

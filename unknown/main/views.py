from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from models import Summoner, Game, Player, Team, SummonerRating, UnkownPlayer
from unknown.rcimport.models import Game as IGame, Player as IPlayer, RunePage, RuneSlot, Summoner as ISummoner, SummonerRankedStatistics, SummonerRating as ISummonerRating, Team as Iteam, UnknownPlayer as IUnknownPlayer
#from rcimport.models import Game, Player, RunePage, RuneSlot, Summoner, SummonerRankedStatistics, SummonerRating, Team, UnknownPlayer


def game_list(request):
	games=IGame.objects.all()[:50]
	qplayer=IPlayer.objects.filter(game__in=games).select_related()
	players={}
	for game in games:
		if game.game_id not in players:
			players[game.game_id]=[]
		cg=qplayer.filter(game=game)
		for p in cg:
			players[game.game_id].append(p.summoner.summoner_name)
	return render_to_response('game_list.html', {'games':games, 'players':players}, RequestContext(request))


def view_game(request, id):
	game=IGame.objects.get(game_id=id)
	players=IPlayer.objects.filter(game=game).order_by('team')
	return render_to_response('view_game.html', {'game':game, 'players':players}, RequestContext(request))

#from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
# from django.shortcuts import render_to_response
from coffin.shortcuts import render_to_response
from django.utils import simplejson
from models import Player, Summoner


def player_info(request, player):
	player=Player.objects.filter(pk=player)
	return HttpResponse(simplejson.dumps(list(player.values())[0]), mimetype='application/json')


def summoner_games(request, summoner):
	summoner=Summoner.objects.get(account_id=summoner)
	g=Player.objects.filter(summoner=summoner).select_related()
	paginator=Paginator(g, 10)
	page=request.GET.get('page')
	try:
		games=paginator.page(page)
	except PageNotAnInteger:
		games=paginator.page(1)
	except EmptyPage:
		games=paginator.page(paginator.num_pages)
	return render_to_response('ajax/summoner_games.html.j2', {'summoner':summoner, 'games':games}, mimetype='text/html')

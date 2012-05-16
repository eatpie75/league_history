from datetime import datetime, timedelta
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from models import Game
from unknown.rcimport.models import Game as IGame, Player as IPlayer, UnknownPlayer as IUnknownPlayer, Summoner as ISummoner
#from unknown.rcimport.models import Game as IGame, Player as IPlayer, RunePage, RuneSlot, Summoner as ISummoner, SummonerRankedStatistics, SummonerRating as ISummonerRating, Team as Iteam, UnknownPlayer as IUnknownPlayer
#from rcimport.models import Game, Player, RunePage, RuneSlot, Summoner, SummonerRankedStatistics, SummonerRating, Team, UnknownPlayer
import requests


def game_list(request):
	games=IGame.objects.with_players(max=25)
	# qplayer=IPlayer.objects.filter(game__in=games).select_related()
	# players={}
	# for game in games:
	# 	if game.game_id not in players:
	# 		players[game.game_id]=[]
	# 	cg=qplayer.filter(game=game)
	# 	for p in cg:
	# 		players[game.game_id].append(p.summoner.summoner_name)
	# return render_to_response('game_list.html', {'games':games, 'players':players}, RequestContext(request))
	return render_to_response('game_list.html', {'games':games}, RequestContext(request))


def view_game(request, id):
	game=IGame.objects.get(game_id=id)
	meta_game=Game.objects.get_or_create(game_id=id)[0]
	#players=IPlayer.objects.filter(game=game).order_by('team').select_related()
	players=IPlayer.objects.filter(Q(team=game.blue_team)|Q(team=game.purple_team)).order_by('team').select_related()
	if len(players)<10 and datetime.fromtimestamp(game.time)>(datetime.utcnow()-timedelta(days=2)) and not meta_game.updated:
		uplayers=IUnknownPlayer.objects.filter(Q(team=game.blue_team)|Q(team=game.purple_team))
		arg=','.join(map(str, uplayers.values_list('summoner_id', flat=True)))
		r=requests.get('http://127.0.0.1:8081/get_names/?ids={}'.format(arg))
		r.encoding='utf-8'
		usummoners=simplejson.loads(unicode(r.text))
		for summoner in usummoners:
			r=requests.get(u'http://127.0.0.1/API/Search/NA/{}'.format(summoner))
			acctid=simplejson.loads(r.text)['AccountId']
			s=simplejson.loads(requests.get('http://127.0.0.1/API/Profile/NA/{}'.format(acctid)).text)
			if not s['Summoner']['HasBeenUpdated']:
				requests.get('http://127.0.0.1/API/Update/NA/{}'.format(acctid))
		meta_game.updated=True
		meta_game.save()
	for player in players:
		if datetime.utcfromtimestamp(player.summoner.time_updated)<(datetime.utcnow()-timedelta(minutes=40)):
			player.summoner._update()
		else:
			#print datetime.utcfromtimestamp(player.summoner.time_updated).isoformat()+" "+(datetime.utcnow()-timedelta(minutes=40)).isoformat()
			pass
	players=IPlayer.objects.filter(game=game).order_by('team').select_related()
	return render_to_response('view_game.html', {'game':game, 'players':players}, RequestContext(request))


def view_summoner(request, acctid, slug):
	summoner=ISummoner.objects.get(account_id=acctid)
	#games=IGame.objects.filter(pk__in=IPlayer.objects.filter(summoner=summoner).only('game__pk').select_related('game__pk').values_list('game__pk', flat=True))
	games=IPlayer.objects.filter(summoner=summoner).select_related('game', 'game__purple_team', 'game__blue_team', 'team')
	return render_to_response('view_summoner.html', {'games':games, 'summoner':summoner}, RequestContext(request))

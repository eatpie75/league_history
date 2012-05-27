from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from django.db.models import Q, Avg
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils import simplejson
from models import Summoner, SummonerRating, Game, Player, fill_game, update_summoners, get_data, REGIONS
from pytz import timezone


def __get_region(region):
	return next(value for value, name in REGIONS if name==region)


def search(request, name):
	from django.http import HttpResponse
	res=get_data('search', {'name':name})
	print res
	return HttpResponse(simplejson.dumps(res), mimetype='application/json')


def game_list(request):
	if 'auto' in request.GET:
		a=Summoner.objects.filter(update_automatically=True)
		b=Player.objects.filter(summoner__in=a, game__fetched=False)
		games=Game.objects.filter(players__in=b).prefetch_related('players', 'players__summoner').select_related()
	else:
		games=Game.objects.all()[:350].prefetch_related('players', 'players__summoner').select_related()
	return render_to_response('game_list.html', {'games':games}, RequestContext(request))


def view_game(request, region, id):
	region=__get_region(region)
	game=Game.objects.get(game_id=id, region=region)
	if game.time>(datetime.utcnow().replace(tzinfo=timezone('UTC'))-timedelta(days=2)) and not game.fetched:
		fill_game(game)
		#tmp=fg.delay(game)
		#tmp.get()
	if game.blue_team_won:
		players=game.players.all().order_by('-blue_team', '-gold').select_related()
	else:
		players=game.players.all().order_by('blue_team', '-gold').select_related()
	modes=('CUSTOM', 'BOT', 'UNRANKED', 'RANKED', 'RANKED TEAM')
	metadata={'map':game.get_game_map_display().upper(), 'mode':modes[game.game_mode]}
	if game.game_mode in (3, 4):
		metadata['avg_elo']=players.aggregate(Avg('rating'))['rating__avg']
	return render_to_response('view_game.html', {'game':game, 'players':players, 'metadata':metadata}, RequestContext(request))


def view_summoner(request, sregion, acctid, slug):
	class Stats(object):
		def __init__(self, games):
			self.games=games
			self.indexed=False
			self.index={}

		def __index(self):
			items={}
			champions={}
			for game in self.games:
				if game.champion_id not in champions:
					champions[game.champion_id]={'count':0, 'won':0, 'lost':0}
				champions[game.champion_id]['count']+=1
				if (game.game.blue_team_won and game.blue_team) or (not game.game.blue_team_won and not game.blue_team):
					champions[game.champion_id]['won']+=1
				else:
					champions[game.champion_id]['lost']+=1
				itt=game.get_items
				for i in itt:
					i=int(i)
					if i==0:
						continue
					if i not in items:
						items[i]={'count':0, 'won':0, 'lost':0}
					items[i]['count']+=1
					if (game.game.blue_team_won and game.blue_team) or (not game.game.blue_team_won and not game.blue_team):
						items[i]['won']+=1
					else:
						items[i]['lost']+=1
			self.index={'champions':champions, 'items':items}
			self.indexed=True

		def most_played(self):
			if not self.indexed: self.__index()
			return sorted(self.index['champions'].iteritems(), key=lambda g:g[1]['count'], reverse=True)

		def best_ratio(self, minimum=3):
			def bsort(g):
				if g[1]['count']>=minimum:
					return g[1]['won']-g[1]['lost']
				else:
					return -100
			if not self.indexed: self.__index()
			return sorted(self.index['champions'].iteritems(), key=bsort, reverse=True)

	region=__get_region(sregion)
	summoner=Summoner.objects.get(account_id=acctid, region=region)
	if slugify(summoner.name)!=slug:
		print slugify(summoner.name)
		print slug
		print reverse('view_summoner', args=[sregion, acctid, slugify(summoner.name)])
		return HttpResponseRedirect(reverse('view_summoner', args=[sregion, acctid, slugify(summoner.name)]))
	if summoner.time_updated<(datetime.utcnow().replace(tzinfo=timezone('UTC'))-timedelta(hours=1)):
		update_summoners(Summoner.objects.filter(account_id=acctid))
		summoner=Summoner.objects.get(account_id=acctid)
	try:
		rating=SummonerRating.objects.get(summoner=summoner, game_map=1, game_mode=3)
	except SummonerRating.DoesNotExist:
		rating=SummonerRating(summoner=summoner, game_map=1, game_mode=3, wins=0, losses=0, leaves=0, current_rating=0, top_rating=0)
		rating.save()
	games=Player.objects.filter(summoner=summoner).select_related()
	return render_to_response('view_summoner.html', {'games':games, 'summoner':summoner, 'rating':rating, 'stats':Stats(games)}, RequestContext(request))


def view_summoner_games(request, region, acctid, slug):
	region=__get_region(region)
	pass


def view_summoner_champions(request, region, acctid, slug):
	region=__get_region(region)
	pass


def view_summoner_specific_champion(request, region, acctid, slug, champion, champion_slug):
	region=__get_region(region)
	pass


def run_auto(request):
	if 'force' in request.GET:
		summoners=Summoner.objects.filter(update_automatically=True)
	else:
		summoners=Summoner.objects.filter(update_automatically=True, time_updated__lt=(datetime.utcnow().replace(tzinfo=timezone('UTC'))-timedelta(hours=3)))
	update_summoners(summoners)
	if 'fill' in request.GET:
		games=Player.objects.filter(summoner__update_automatically=True, game__fetched=False, game__time__gt=(datetime.utcnow().replace(tzinfo=timezone('UTC'))-timedelta(days=2)))
		for player in games:
			fill_game(player.game)
	return render_to_response('run_auto.html', {'summoners':summoners}, RequestContext(request))

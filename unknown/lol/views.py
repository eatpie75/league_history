from core.stats import Stats
from datetime import datetime, timedelta
from django import forms
# from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.db.models import Q, Avg
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils import simplejson
from models import Summoner, SummonerRating, Game, Player, fill_game, update_summoners, get_data, REGIONS, MAPS, MODES
from pytz import timezone


def __get_region(region):
	return next(value for value, name in REGIONS if name==region)


def __get_rating(summoner):
	try:
		rating=SummonerRating.objects.get(summoner=summoner, game_map=1, game_mode=3)
	except SummonerRating.DoesNotExist:
		rating=SummonerRating(summoner=summoner, game_map=1, game_mode=3, wins=0, losses=0, leaves=0, current_rating=0, top_rating=0)
		rating.save()
	return rating


def search(request, name):
	from django.http import HttpResponse
	res=get_data('search', {'name':name})
	print res
	return HttpResponse(simplejson.dumps(res), mimetype='application/json')


def game_list(request):
	if 'auto' in request.GET:
		a=Summoner.objects.filter(update_automatically=True)
		b=Player.objects.filter(summoner__in=a, game__fetched=False)
		games=Game.objects.filter(players__in=b).prefetch_related('players', 'players__summoner').select_related().distinct()
	else:
		games=Game.objects.all()[:350].prefetch_related('players', 'players__summoner').select_related()
	return render_to_response('game_list.html', {'games':games}, RequestContext(request))


# @cache_page(60 * 60)
def view_game(request, region, id):
	region=__get_region(region)
	game=Game.objects.get(game_id=id, region=region)
	if game.time>(datetime.utcnow().replace(tzinfo=timezone('UTC'))-timedelta(days=2)) and not game.fetched:
		fill_game(game)
	if game.blue_team_won:
		players=game.players.all().order_by('-blue_team', '-gold').select_related()
	else:
		players=game.players.all().order_by('blue_team', '-gold').select_related()
	modes=('CUSTOM', 'BOT', 'UNRANKED', 'RANKED', 'RANKED TEAM')
	metadata={'map':game.get_game_map_display().upper(), 'mode':modes[game.game_mode]}
	if game.game_mode in (3, 4):
		metadata['avg_elo']=players.aggregate(Avg('rating'))['rating__avg']
	return render_to_response('view_game.html', {'game':game, 'players':players, 'metadata':metadata}, RequestContext(request))


# @cache_page(60 * 15)
def view_summoner(request, sregion, acctid, slug):
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
	rating=__get_rating(summoner)
	games=Player.objects.filter(summoner=summoner).select_related()
	stats=Stats(games)
	return render_to_response('view_summoner.html', {'games':games, 'summoner':summoner, 'rating':rating, 'stats':stats}, RequestContext(request))


# @cache_page(60 * 15)
def view_summoner_games(request, sregion, acctid, slug):
	region=__get_region(sregion)
	summoner=Summoner.objects.get(account_id=acctid, region=region)
	if slugify(summoner.name)!=slug:
		print slugify(summoner.name)
		print slug
		print reverse('view_summoner_games', args=[sregion, acctid, slugify(summoner.name)])
		return HttpResponseRedirect(reverse('view_summoner', args=[sregion, acctid, slugify(summoner.name)]))
	rating=__get_rating(summoner)
	games=Player.objects.filter(summoner=summoner).select_related()
	return render_to_response('view_summoner_games.html', {'games':Paginator(games, 10).page(1), 'summoner':summoner, 'rating':rating, 'stats':Stats(games)}, RequestContext(request))


# @cache_page(60 * 15)
def view_summoner_champions(request, sregion, acctid, slug):
	from core.champions import CHAMPIONS
	region=__get_region(sregion)
	summoner=Summoner.objects.get(account_id=acctid, region=region)
	if slugify(summoner.name)!=slug:
		print slugify(summoner.name)
		print slug
		print reverse('view_summoner_champions', args=[sregion, acctid, slugify(summoner.name)])
		return HttpResponseRedirect(reverse('view_summoner_champions', args=[sregion, acctid, slugify(summoner.name)]))
	rating=__get_rating(summoner)
	games=Player.objects.filter(summoner=summoner).select_related()
	stats=Stats(games)
	# assert False
	return render_to_response('view_summoner_champions.html', {'games':games, 'summoner':summoner, 'rating':rating, 'stats':stats, 'champions':CHAMPIONS}, RequestContext(request))


def view_summoner_specific_champion(request, sregion, acctid, slug, champion, champion_slug):
	from core.champions import CHAMPIONS
	region=__get_region(sregion)
	summoner=Summoner.objects.get(account_id=acctid, region=region)
	if slugify(summoner.name)!=slug:
		print slugify(summoner.name)
		print slug
		print reverse('view_summoner_specific_champion', args=[sregion, acctid, slugify(summoner.name), champion, champion_slug])
		return HttpResponseRedirect(reverse('view_summoner_specific_champion', args=[sregion, acctid, slugify(summoner.name), champion, champion_slug]))
	rating=__get_rating(summoner)
	games=Player.objects.filter(summoner=summoner, champion_id=champion).select_related()
	stats=Stats(games, champion)
	return render_to_response('view_summoner_specific_champion.html', {'games':games, 'summoner':summoner, 'rating':rating, 'stats':stats, 'champions':CHAMPIONS, 'champion': champion}, RequestContext(request))


@cache_page(60 * 60)
def view_all_champions(request):
	from core.champions import CHAMPIONS
	from django.db.models import Count

	class MapModeForm(forms.Form):
		maps=[(-1, 'All maps'),]
		maps.extend(MAPS)
		modes=[(-1, 'All modes'),]
		modes.extend(MODES)
		game_map=forms.ChoiceField(required=False, choices=maps[:-1], widget=forms.Select(attrs={'class':'span2'}))
		game_mode=forms.ChoiceField(required=False, choices=modes[:-1], widget=forms.Select(attrs={'class':'span2'}))
	form=MapModeForm(request.GET)
	form.is_valid()
	games=Player.objects.all()
	if form.cleaned_data['game_map'] not in ('', '-1'):
		games=games.filter(game__game_map=form.cleaned_data['game_map'])
	if form.cleaned_data['game_mode'] not in ('', '-1'):
		games=games.filter(game__game_mode=form.cleaned_data['game_mode'])
	stats=Stats(games)
	count=games.aggregate(Count('game', distinct=True))['game__count']
	return render_to_response('view_all_champions.html', {'games':games, 'stats':stats, 'champions':CHAMPIONS, 'form':form, 'count':count}, RequestContext(request))


# @cache_page(60 * 60)
def view_champion(request, champion, champion_slug):
	from core.champions import CHAMPIONS
	from core.items import ITEMS

	class MapModeForm(forms.Form):
		maps=[(-1, 'All maps'),]
		maps.extend(MAPS)
		modes=[(-1, 'All modes'),]
		modes.extend(MODES)
		game_map=forms.ChoiceField(required=False, choices=maps[:-1], widget=forms.Select(attrs={'class':'span2'}))
		game_mode=forms.ChoiceField(required=False, choices=modes[:-1], widget=forms.Select(attrs={'class':'span2'}))
	form=MapModeForm(request.GET)
	form.is_valid()
	print form.cleaned_data
	games=Player.objects.filter(champion_id=champion)
	if form.cleaned_data['game_map'] not in ('', '-1'):
		games=games.filter(game__game_map=form.cleaned_data['game_map'])
	if form.cleaned_data['game_mode'] not in ('', '-1'):
		games=games.filter(game__game_mode=form.cleaned_data['game_mode'])
	stats=Stats(games, champion)
	return render_to_response('view_champion.html', {'games':games, 'stats':stats, 'champions':CHAMPIONS, 'items':ITEMS, 'form':form, 'champion':int(champion)}, RequestContext(request))


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

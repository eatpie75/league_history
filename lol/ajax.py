from datetime import datetime, timedelta
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from lol.tasks import summoner_auto_task
from lol.models import Player, Summoner
from pytz import timezone
import json


def player_info(request, player):
	player=Player.objects.filter(pk=player)
	result=player.values()[0]
	result['gpm']=player[0].gpm
	return HttpResponse(json.dumps(result), mimetype='application/json')


def summoner_games(request, region, account_id):
	summoner=Summoner.objects.get(region=region, account_id=account_id)
	g=Player.objects.filter(summoner=summoner).select_related()
	paginator=Paginator(g, 10)
	page=request.GET.get('page')
	try:
		games=paginator.page(page)
	except PageNotAnInteger:
		games=paginator.page(1)
	except EmptyPage:
		games=paginator.page(paginator.num_pages)
	return render_to_response('ajax/summoner_games.html.j2', {'summoner':summoner, 'games':games}, RequestContext(request), mimetype='text/html')


def force_update(request, region, account_id):
	summoner=Summoner.objects.get(region=region, account_id=account_id)
	c=cache.get('summoner/{}/{}/updating'.format(region, account_id))
	if c is not None or summoner.time_updated>(datetime.now(timezone('UTC'))-timedelta(minutes=30)):
		return HttpResponse(json.dumps({'status':'DONE', 'msg':'REFRESH PAGE TO SEE UPDATED STATS'}), mimetype='application/json')
	summoner_auto_task.apply_async(args=[summoner.pk,], ignore_result=True, priority=0)
	return HttpResponse(json.dumps({'status':'QUEUE', 'msg':'UPDATE IN QUEUE', 'delay':3000}), mimetype='application/json')


def force_update_status(request, region, account_id):
	if cache.get('summoner/{}/{}/updating'.format(region, account_id)) is not None:
		return HttpResponse(json.dumps({'status':'QUEUE', 'delay':3000}), mimetype='application/json')
	else:
		return HttpResponse(json.dumps({'status':'DONE', 'msg':'REFRESH PAGE TO SEE UPDATED STATS'}), mimetype='application/json')

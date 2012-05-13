from django.db import models
from datetime import datetime, timedelta
import requests

MAPS=((0, 'Twisted Treeline'), (1, 'Summoners Rift'), (2, 'Dominion'))
MODES=((0, 'Custom'), (1, 'Bot'), (2, 'Normal'), (3, 'Solo'), (4, 'Premade'))
REGIONS=((0, 'NA'), (1, 'EUW'), (2, 'EUNE'))


class GameManager(models.Manager):
	def with_players(self, max=25, *args, **kwargs):
		qs=self.get_query_set().filter(*args, **kwargs)[:max]
		allplayers=Player.objects.filter(game__in=qs).select_related('summoner').only('summoner__summoner_name', 'summoner__account_id')
		i=0
		for q in qs:
			setattr(qs[i], 'players', allplayers.filter(game=q))
			i+=1
		return qs


class Game(models.Model):
	id=models.IntegerField(primary_key=True)
	game_id=models.IntegerField()
	map=models.IntegerField(choices=MAPS, db_index=True)
	game_mode=models.IntegerField(choices=MODES, db_index=True)
	time=models.IntegerField()
	blue_team=models.ForeignKey('Team', related_name='bteam', db_index=True)
	purple_team=models.ForeignKey('Team', related_name='pteam', db_index=True)
	blue_team_won=models.IntegerField()

	def _time_display(self):
		return datetime.fromtimestamp(self.time)

	def _get_players(self):
		return Player.objects.filter(game=self).select_related()

	def __unicode__(self):
		#return datetime.utcfromtimestamp(self.time).isoformat()
		return unicode(self.game_id)
	time_display=property(_time_display)
	objects=GameManager()
	#players=property(_get_players)

	class Meta:
		db_table=u'game'
		ordering=['-time',]


class Player(models.Model):
	rowid=models.IntegerField(primary_key=True)
	game=models.ForeignKey(Game, db_index=True)
	team=models.ForeignKey('Team', db_index=True)
	summoner=models.ForeignKey('Summoner', db_index=True)
	ping=models.IntegerField()
	time_spent_in_queue=models.IntegerField()
	premade_size=models.IntegerField()
	experience_earned=models.IntegerField()
	boosted_experience_earned=models.IntegerField()
	ip_earned=models.IntegerField()
	boosted_ip_earned=models.IntegerField()
	summoner_level=models.IntegerField()
	summoner_spell1=models.IntegerField()
	summoner_spell2=models.IntegerField()
	champion_id=models.IntegerField()
	skin_name=models.CharField(max_length=64, blank=True)
	skin_index=models.IntegerField()
	champion_level=models.IntegerField()
	items=models.TextField()  # This field type is a guess.
	kills=models.IntegerField()
	deaths=models.IntegerField()
	assists=models.IntegerField()
	minion_kills=models.IntegerField()
	gold=models.IntegerField()
	damage_dealt=models.IntegerField()
	physical_damage_dealt=models.IntegerField()
	magical_damage_dealt=models.IntegerField()
	damage_taken=models.IntegerField()
	physical_damage_taken=models.IntegerField()
	magical_damage_taken=models.IntegerField()
	total_healing_done=models.IntegerField()
	time_spent_dead=models.IntegerField()
	largest_multikill=models.IntegerField()
	largest_killing_spree=models.IntegerField()
	largest_critical_strike=models.IntegerField()
	neutral_minions_killed=models.IntegerField(null=True, blank=True)
	turrets_destroyed=models.IntegerField(null=True, blank=True)
	inhibitors_destroyed=models.IntegerField(null=True, blank=True)
	nodes_neutralised=models.IntegerField(null=True, blank=True)
	node_neutralisation_assists=models.IntegerField(null=True, blank=True)
	nodes_captured=models.IntegerField(null=True, blank=True)
	victory_points=models.IntegerField(null=True, blank=True)
	objectives=models.IntegerField(null=True, blank=True)
	total_score=models.IntegerField(null=True, blank=True)
	objective_score=models.IntegerField(null=True, blank=True)
	combat_score=models.IntegerField(null=True, blank=True)
	rank=models.IntegerField(null=True, blank=True)

	def _get_items(self):
		return self.items.strip("'{}").split(', ')
	get_items=property(_get_items)

	def __unicode__(self):
		return unicode(self.summoner.summoner_name)

	class Meta:
		db_table=u'player'
		ordering=['game',]


class RunePage(models.Model):
	id=models.IntegerField(primary_key=True)
	summoner=models.ForeignKey('Summoner', db_index=True)
	name=models.CharField(max_length=64)
	is_current_rune_page=models.IntegerField()
	time_created=models.IntegerField()

	def __unicode__(self):
		return self.name

	class Meta:
		db_table=u'rune_page'


class RuneSlot(models.Model):
	rune_page_id=models.ForeignKey(RunePage, db_index=True)
	rune_slot=models.IntegerField()
	rune=models.IntegerField()

	class Meta:
		db_table=u'rune_slot'


class Summoner(models.Model):
	id=models.IntegerField(primary_key=True)
	region=models.IntegerField(choices=REGIONS)
	account_id=models.IntegerField(unique=True, db_index=True)
	summoner_id=models.IntegerField()
	summoner_name=models.CharField(max_length=64, db_index=True)
	internal_name=models.CharField(max_length=64)
	summoner_level=models.IntegerField()
	profile_icon=models.IntegerField()
	has_been_updated=models.IntegerField()
	update_automatically=models.IntegerField(db_index=True)
	time_created=models.IntegerField()
	time_updated=models.IntegerField()

	def _update(self):
		print "Updating {}".format(self.summoner_name)
		requests.get('http://127.0.0.1/API/Update/NA/{}'.format(self.account_id))
		return self

	def _get_and_update(self):
		last_updated=datetime.utcfromtimestamp(self.time_updated)
		if last_updated<(datetime.utcnow()-timedelta(hours=4)):
			self._update()
		return self
	get_and_update=property(_get_and_update)

	def __unicode__(self):
		return unicode(self.summoner_name)

	class Meta:
		db_table=u'summoner'


class SummonerRankedStatistics(models.Model):
	summoner=models.ForeignKey(Summoner, db_index=True)
	season=models.IntegerField()
	champion_id=models.IntegerField()
	wins=models.IntegerField()
	losses=models.IntegerField()
	kills=models.IntegerField()
	deaths=models.IntegerField()
	assists=models.IntegerField()
	minion_kills=models.IntegerField()
	gold=models.IntegerField()
	turrets_destroyed=models.IntegerField()
	damage_dealt=models.IntegerField()
	physical_damage_dealt=models.IntegerField()
	magical_damage_dealt=models.IntegerField()
	damage_taken=models.IntegerField()
	double_kills=models.IntegerField()
	triple_kills=models.IntegerField()
	quadra_kills=models.IntegerField()
	penta_kills=models.IntegerField()
	time_spent_dead=models.IntegerField()
	maximum_kills=models.IntegerField()
	maximum_deaths=models.IntegerField()

	class Meta:
		db_table=u'summoner_ranked_statistics'


class SummonerRating(models.Model):
	summoner=models.ForeignKey(Summoner, db_index=True)
	map=models.IntegerField(db_index=True)
	game_mode=models.IntegerField(db_index=True)
	wins=models.IntegerField()
	losses=models.IntegerField()
	leaves=models.IntegerField()
	current_rating=models.IntegerField(null=True, blank=True)
	top_rating=models.IntegerField(null=True, blank=True)

	class Meta:
		db_table=u'summoner_rating'


class Team(models.Model):
	id=models.IntegerField(primary_key=True)

	def __unicode__(self):
		return unicode(self.id)

	class Meta:
		db_table=u'team'


class UnknownPlayer(models.Model):
	rowid=models.IntegerField(primary_key=True)
	team=models.ForeignKey(Team)
	champion_id=models.IntegerField()
	summoner_id=models.IntegerField()

	def __unicode__(self):
		return unicode(self.summoner_id)

	class Meta:
		db_table=u'unknown_player'
		ordering=['rowid',]

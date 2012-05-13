from django.db import models
#from datetime import datetime

MAPS=((0, 'Twisted Treeline'), (1, 'Summoners Rift'), (2, 'Dominion'))
MODES=((0, 'Custom'), (1, 'Bot'), (2, 'Normal'), (3, 'Solo'), (4, 'Premade'))
REGIONS=((0, 'NA'), (1, 'EUW'), (2, 'EUNE'))


# class Item(models.Model):
# 	item_id=models.IntegerField()
# 	name=models.CharField(max_length=64)
# 	description=models.TextField()

# 	def __unicode__(self):
# 		return self.name


# class Summoner(models.Model):
# 	id=models.IntegerField(primary_key=True)
# 	region=models.IntegerField(choices=REGIONS)
# 	account_id=models.IntegerField(unique=True, db_index=True)
# 	summoner_id=models.IntegerField()
# 	name=models.CharField(max_length=64, db_index=True)
# 	internal_name=models.CharField(max_length=64)
# 	level=models.IntegerField()
# 	profile_icon=models.IntegerField()
# 	has_been_updated=models.IntegerField()
# 	update_automatically=models.IntegerField(db_index=True)
# 	time_created=models.DateTimeField()
# 	time_updated=models.DateTimeField()

# 	def __unicode__(self):
# 		return self.summoner_name


class Game(models.Model):
	game_id=models.IntegerField()
	updated=models.BooleanField(default=False)

	def __unicode__(self):
		return unicode(self.game_id)


# class Player(models.Model):
# 	game=models.ForeignKey(Game, null=True, blank=True, db_index=True)
# 	team=models.ForeignKey('Team', db_index=True)
# 	summoner=models.ForeignKey('Summoner', db_index=True)
# 	ping=models.IntegerField()
# 	time_spent_in_queue=models.IntegerField()
# 	premade_size=models.IntegerField()
# 	experience_earned=models.IntegerField()
# 	boosted_experience_earned=models.IntegerField()
# 	ip_earned=models.IntegerField()
# 	boosted_ip_earned=models.IntegerField()
# 	summoner_level=models.IntegerField()
# 	summoner_spell1=models.IntegerField()
# 	summoner_spell2=models.IntegerField()
# 	champion_id=models.IntegerField()
# 	skin_name=models.CharField(max_length=64, blank=True)
# 	skin_index=models.IntegerField()
# 	champion_level=models.IntegerField()
# 	items=models.CommaSeparatedIntegerField(max_length=128)
# 	kills=models.IntegerField()
# 	deaths=models.IntegerField()
# 	assists=models.IntegerField()
# 	minion_kills=models.IntegerField()
# 	gold=models.IntegerField()
# 	damage_dealt=models.IntegerField()
# 	physical_damage_dealt=models.IntegerField()
# 	magical_damage_dealt=models.IntegerField()
# 	damage_taken=models.IntegerField()
# 	physical_damage_taken=models.IntegerField()
# 	magical_damage_taken=models.IntegerField()
# 	total_healing_done=models.IntegerField()
# 	time_spent_dead=models.IntegerField()
# 	largest_multikill=models.IntegerField()
# 	largest_killing_spree=models.IntegerField()
# 	largest_critical_strike=models.IntegerField()
# 	neutral_minions_killed=models.IntegerField(null=True, blank=True)
# 	turrets_destroyed=models.IntegerField(null=True, blank=True)
# 	inhibitors_destroyed=models.IntegerField(null=True, blank=True)
# 	nodes_neutralised=models.IntegerField(null=True, blank=True)
# 	node_neutralisation_assists=models.IntegerField(null=True, blank=True)
# 	nodes_captured=models.IntegerField(null=True, blank=True)
# 	victory_points=models.IntegerField(null=True, blank=True)
# 	objectives=models.IntegerField(null=True, blank=True)
# 	total_score=models.IntegerField(null=True, blank=True)
# 	objective_score=models.IntegerField(null=True, blank=True)
# 	combat_score=models.IntegerField(null=True, blank=True)
# 	rank=models.IntegerField(null=True, blank=True)

# 	def __unicode__(self):
# 		return '{0} - {1}'.format(self.game.game_id, self.summoner.summoner_name)

# 	class Meta:
# 		ordering=['game', ]


# class Team(models.Model):
# 	id=models.IntegerField(primary_key=True)

# 	def __unicode__(self):
# 		return unicode(self.id)


# class SummonerRating(models.Model):
# 	summoner=models.ForeignKey(Summoner, db_index=True)
# 	map=models.IntegerField(choices=MAPS, db_index=True)
# 	game_mode=models.IntegerField(choices=MODES, db_index=True)
# 	wins=models.IntegerField()
# 	losses=models.IntegerField()
# 	leaves=models.IntegerField()
# 	current_rating=models.IntegerField(null=True, blank=True)
# 	top_rating=models.IntegerField(null=True, blank=True)


# class UnknownPlayer(models.Model):
# 	last_retrieved=models.IntegerField()

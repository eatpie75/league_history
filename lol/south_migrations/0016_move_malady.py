# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):

	def forwards(self, orm):
		"Write your forwards methods here."
		# Note: Don't use "from appname.models import ModelName".
		# Use orm.ModelName to refer to models in this application,
		# and orm['appname.ModelName'] for models in other applications.
		for player in orm['lol.player'].objects.filter(items__contains='|3114|', game__time__lt=datetime.datetime(year=2013, month=6, day=13)):
			items=player.items.split('|')[1:-1]
			new_items=[]
			for item in items:
				if item=='3114':
					new_items.append('9002')
				else:
					new_items.append(item)
			player.items='|' + '|'.join(new_items) + '|'
			player.save()

	def backwards(self, orm):
		raise RuntimeError("Cannot reverse this migration.")

	models = {
		u'lol.game': {
			'Meta': {'ordering': "['-time']", 'unique_together': "(('region', 'game_id'),)", 'object_name': 'Game', 'index_together': "[('game_map', 'game_mode'), ('game_id', 'region')]"},
			'blue_team_won': ('django.db.models.fields.BooleanField', [], {}),
			'fetched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'game_id': ('django.db.models.fields.IntegerField', [], {}),
			'game_map': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
			'game_mode': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'invalid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'region': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
			'time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
			'unfetched_players': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
		},
		u'lol.player': {
			'Meta': {'ordering': "['game']", 'unique_together': "(('game', 'summoner'),)", 'object_name': 'Player'},
			'afk': ('django.db.models.fields.BooleanField', [], {}),
			'assists': ('django.db.models.fields.IntegerField', [], {}),
			'blue_team': ('django.db.models.fields.BooleanField', [], {}),
			'boosted_experience_earned': ('django.db.models.fields.IntegerField', [], {}),
			'boosted_ip_earned': ('django.db.models.fields.IntegerField', [], {}),
			'champion_id': ('django.db.models.fields.IntegerField', [], {}),
			'champion_level': ('django.db.models.fields.IntegerField', [], {}),
			'combat_player_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
			'damage_dealt': ('django.db.models.fields.IntegerField', [], {}),
			'damage_taken': ('django.db.models.fields.IntegerField', [], {}),
			'deaths': ('django.db.models.fields.IntegerField', [], {}),
			'division': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
			'experience_earned': ('django.db.models.fields.IntegerField', [], {}),
			'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lol.Game']"}),
			'gold': ('django.db.models.fields.IntegerField', [], {}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'inhibitors_destroyed': ('django.db.models.fields.IntegerField', [], {}),
			'ip_earned': ('django.db.models.fields.IntegerField', [], {}),
			'items': ('django.db.models.fields.CharField', [], {'max_length': '43'}),
			'kills': ('django.db.models.fields.IntegerField', [], {}),
			'largest_critical_strike': ('django.db.models.fields.IntegerField', [], {}),
			'largest_killing_spree': ('django.db.models.fields.IntegerField', [], {}),
			'largest_multikill': ('django.db.models.fields.IntegerField', [], {}),
			'leaver': ('django.db.models.fields.BooleanField', [], {}),
			'magic_damage_dealt': ('django.db.models.fields.IntegerField', [], {}),
			'magic_damage_taken': ('django.db.models.fields.IntegerField', [], {}),
			'minion_kills': ('django.db.models.fields.IntegerField', [], {}),
			'neutral_minions_killed': ('django.db.models.fields.IntegerField', [], {}),
			'neutral_minions_killed_enemy_jungle': ('django.db.models.fields.IntegerField', [], {}),
			'neutral_minions_killed_your_jungle': ('django.db.models.fields.IntegerField', [], {}),
			'node_capture': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
			'node_capture_assist': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
			'node_neutralize': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
			'node_neutralize_assist': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
			'objective_player_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
			'physical_damage_dealt': ('django.db.models.fields.IntegerField', [], {}),
			'physical_damage_taken': ('django.db.models.fields.IntegerField', [], {}),
			'ping': ('django.db.models.fields.IntegerField', [], {}),
			'premade_size': ('django.db.models.fields.IntegerField', [], {}),
			'queue_length': ('django.db.models.fields.IntegerField', [], {}),
			'rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
			'sight_wards_bought_in_game': ('django.db.models.fields.IntegerField', [], {}),
			'skin_index': ('django.db.models.fields.IntegerField', [], {}),
			'skin_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
			'summoner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lol.Summoner']"}),
			'summoner_level': ('django.db.models.fields.IntegerField', [], {}),
			'summoner_spell1': ('django.db.models.fields.IntegerField', [], {}),
			'summoner_spell2': ('django.db.models.fields.IntegerField', [], {}),
			'team_objective': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
			'tier': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
			'time_spent_dead': ('django.db.models.fields.IntegerField', [], {}),
			'total_healing_done': ('django.db.models.fields.IntegerField', [], {}),
			'total_player_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
			'total_score_rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
			'total_time_crowd_control_dealt': ('django.db.models.fields.IntegerField', [], {}),
			'true_damage_dealt': ('django.db.models.fields.IntegerField', [], {}),
			'true_damage_taken': ('django.db.models.fields.IntegerField', [], {}),
			'turrets_destroyed': ('django.db.models.fields.IntegerField', [], {}),
			'victory_point_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
			'vision_wards_bought_in_game': ('django.db.models.fields.IntegerField', [], {}),
			'ward_killed': ('django.db.models.fields.IntegerField', [], {}),
			'ward_placed': ('django.db.models.fields.IntegerField', [], {}),
			'won': ('django.db.models.fields.BooleanField', [], {})
		},
		u'lol.summoner': {
			'Meta': {'unique_together': "(('region', 'account_id'),)", 'object_name': 'Summoner', 'index_together': "[('region', 'account_id')]"},
			'account_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
			'fully_update': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
			'level': ('django.db.models.fields.IntegerField', [], {}),
			'masteries': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'blank': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
			'profile_icon': ('django.db.models.fields.IntegerField', [], {}),
			'region': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
			'runes': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'blank': 'True'}),
			'summoner_id': ('django.db.models.fields.IntegerField', [], {}),
			'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
			'time_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 25, 0, 0)'}),
			'update_automatically': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'})
		},
		u'lol.summonerrankedstatistics': {
			'Meta': {'object_name': 'SummonerRankedStatistics'},
			'assists': ('django.db.models.fields.IntegerField', [], {}),
			'champion_id': ('django.db.models.fields.IntegerField', [], {}),
			'damage_dealt': ('django.db.models.fields.IntegerField', [], {}),
			'damage_taken': ('django.db.models.fields.IntegerField', [], {}),
			'deaths': ('django.db.models.fields.IntegerField', [], {}),
			'double_kills': ('django.db.models.fields.IntegerField', [], {}),
			'gold': ('django.db.models.fields.IntegerField', [], {}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'kills': ('django.db.models.fields.IntegerField', [], {}),
			'losses': ('django.db.models.fields.IntegerField', [], {}),
			'magical_damage_dealt': ('django.db.models.fields.IntegerField', [], {}),
			'maximum_deaths': ('django.db.models.fields.IntegerField', [], {}),
			'maximum_kills': ('django.db.models.fields.IntegerField', [], {}),
			'minion_kills': ('django.db.models.fields.IntegerField', [], {}),
			'penta_kills': ('django.db.models.fields.IntegerField', [], {}),
			'physical_damage_dealt': ('django.db.models.fields.IntegerField', [], {}),
			'quadra_kills': ('django.db.models.fields.IntegerField', [], {}),
			'season': ('django.db.models.fields.IntegerField', [], {}),
			'summoner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lol.Summoner']"}),
			'time_spent_dead': ('django.db.models.fields.IntegerField', [], {}),
			'triple_kills': ('django.db.models.fields.IntegerField', [], {}),
			'turrets_destroyed': ('django.db.models.fields.IntegerField', [], {}),
			'wins': ('django.db.models.fields.IntegerField', [], {})
		},
		u'lol.summonerrating': {
			'Meta': {'unique_together': "(('summoner', 'game_map', 'game_mode'),)", 'object_name': 'SummonerRating', 'index_together': "[('summoner', 'game_map', 'game_mode')]"},
			'division': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
			'game_map': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
			'game_mode': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'league': ('django.db.models.fields.CharField', [], {'max_length': '127', 'null': 'True', 'blank': 'True'}),
			'losses': ('django.db.models.fields.IntegerField', [], {}),
			'miniseries_losses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
			'miniseries_target': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
			'miniseries_wins': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
			'rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
			'summoner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lol.Summoner']"}),
			'tier': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
			'wins': ('django.db.models.fields.IntegerField', [], {})
		}
	}

	complete_apps = ['lol']
	symmetrical = True

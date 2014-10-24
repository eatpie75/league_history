# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Player.rank'
        db.delete_column('lol_player', 'rank')

        # Deleting field 'Player.nodes_neutralised'
        db.delete_column('lol_player', 'nodes_neutralised')

        # Deleting field 'Player.node_neutralisation_assists'
        db.delete_column('lol_player', 'node_neutralisation_assists')

        # Deleting field 'Player.combat_score'
        db.delete_column('lol_player', 'combat_score')

        # Deleting field 'Player.total_score'
        db.delete_column('lol_player', 'total_score')

        # Deleting field 'Player.victory_points'
        db.delete_column('lol_player', 'victory_points')

        # Deleting field 'Player.objective_score'
        db.delete_column('lol_player', 'objective_score')

        # Deleting field 'Player.nodes_captured'
        db.delete_column('lol_player', 'nodes_captured')

        # Deleting field 'Player.objectives'
        db.delete_column('lol_player', 'objectives')

        # Adding field 'Player.vision_wards_bought_in_game'
        db.add_column('lol_player', 'vision_wards_bought_in_game',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Player.node_neutralize'
        db.add_column('lol_player', 'node_neutralize',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Player.node_neutralize_assist'
        db.add_column('lol_player', 'node_neutralize_assist',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Player.node_capture'
        db.add_column('lol_player', 'node_capture',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Player.node_capture_assist'
        db.add_column('lol_player', 'node_capture_assist',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Player.victory_point_total'
        db.add_column('lol_player', 'victory_point_total',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Player.team_objective'
        db.add_column('lol_player', 'team_objective',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Player.total_player_score'
        db.add_column('lol_player', 'total_player_score',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Player.objective_player_score'
        db.add_column('lol_player', 'objective_player_score',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Player.combat_player_score'
        db.add_column('lol_player', 'combat_player_score',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Player.total_score_rank'
        db.add_column('lol_player', 'total_score_rank',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Player.rank'
        db.add_column('lol_player', 'rank',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Player.nodes_neutralised'
        db.add_column('lol_player', 'nodes_neutralised',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Player.node_neutralisation_assists'
        db.add_column('lol_player', 'node_neutralisation_assists',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Player.combat_score'
        db.add_column('lol_player', 'combat_score',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Player.total_score'
        db.add_column('lol_player', 'total_score',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Player.victory_points'
        db.add_column('lol_player', 'victory_points',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Player.objective_score'
        db.add_column('lol_player', 'objective_score',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Player.nodes_captured'
        db.add_column('lol_player', 'nodes_captured',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Player.objectives'
        db.add_column('lol_player', 'objectives',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Player.vision_wards_bought_in_game'
        db.delete_column('lol_player', 'vision_wards_bought_in_game')

        # Deleting field 'Player.node_neutralize'
        db.delete_column('lol_player', 'node_neutralize')

        # Deleting field 'Player.node_neutralize_assist'
        db.delete_column('lol_player', 'node_neutralize_assist')

        # Deleting field 'Player.node_capture'
        db.delete_column('lol_player', 'node_capture')

        # Deleting field 'Player.node_capture_assist'
        db.delete_column('lol_player', 'node_capture_assist')

        # Deleting field 'Player.victory_point_total'
        db.delete_column('lol_player', 'victory_point_total')

        # Deleting field 'Player.team_objective'
        db.delete_column('lol_player', 'team_objective')

        # Deleting field 'Player.total_player_score'
        db.delete_column('lol_player', 'total_player_score')

        # Deleting field 'Player.objective_player_score'
        db.delete_column('lol_player', 'objective_player_score')

        # Deleting field 'Player.combat_player_score'
        db.delete_column('lol_player', 'combat_player_score')

        # Deleting field 'Player.total_score_rank'
        db.delete_column('lol_player', 'total_score_rank')


    models = {
        'lol.game': {
            'Meta': {'ordering': "['-time']", 'unique_together': "(('region', 'game_id'),)", 'object_name': 'Game'},
            'blue_team_won': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fetched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'game_id': ('django.db.models.fields.IntegerField', [], {}),
            'game_map': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'game_mode': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invalid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'region': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'unfetched_players': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
        },
        'lol.player': {
            'Meta': {'ordering': "['game']", 'unique_together': "(('game', 'summoner'),)", 'object_name': 'Player'},
            'afk': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assists': ('django.db.models.fields.IntegerField', [], {}),
            'blue_team': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'boosted_experience_earned': ('django.db.models.fields.IntegerField', [], {}),
            'boosted_ip_earned': ('django.db.models.fields.IntegerField', [], {}),
            'champion_id': ('django.db.models.fields.IntegerField', [], {}),
            'champion_level': ('django.db.models.fields.IntegerField', [], {}),
            'combat_player_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'damage_dealt': ('django.db.models.fields.IntegerField', [], {}),
            'damage_taken': ('django.db.models.fields.IntegerField', [], {}),
            'deaths': ('django.db.models.fields.IntegerField', [], {}),
            'experience_earned': ('django.db.models.fields.IntegerField', [], {}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lol.Game']"}),
            'gold': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inhibitors_destroyed': ('django.db.models.fields.IntegerField', [], {}),
            'ip_earned': ('django.db.models.fields.IntegerField', [], {}),
            'items': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'kills': ('django.db.models.fields.IntegerField', [], {}),
            'largest_critical_strike': ('django.db.models.fields.IntegerField', [], {}),
            'largest_killing_spree': ('django.db.models.fields.IntegerField', [], {}),
            'largest_multikill': ('django.db.models.fields.IntegerField', [], {}),
            'leaver': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'magic_damage_dealt': ('django.db.models.fields.IntegerField', [], {}),
            'magic_damage_taken': ('django.db.models.fields.IntegerField', [], {}),
            'minion_kills': ('django.db.models.fields.IntegerField', [], {}),
            'neutral_minions_killed': ('django.db.models.fields.IntegerField', [], {}),
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
            'rating': ('django.db.models.fields.IntegerField', [], {}),
            'sight_wards_bought_in_game': ('django.db.models.fields.IntegerField', [], {}),
            'skin_index': ('django.db.models.fields.IntegerField', [], {}),
            'skin_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'summoner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lol.Summoner']"}),
            'summoner_level': ('django.db.models.fields.IntegerField', [], {}),
            'summoner_spell1': ('django.db.models.fields.IntegerField', [], {}),
            'summoner_spell2': ('django.db.models.fields.IntegerField', [], {}),
            'team_objective': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'time_spent_dead': ('django.db.models.fields.IntegerField', [], {}),
            'total_healing_done': ('django.db.models.fields.IntegerField', [], {}),
            'total_player_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_score_rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'turrets_destroyed': ('django.db.models.fields.IntegerField', [], {}),
            'victory_point_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vision_wards_bought_in_game': ('django.db.models.fields.IntegerField', [], {}),
            'won': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'lol.summoner': {
            'Meta': {'unique_together': "(('region', 'account_id'),)", 'object_name': 'Summoner'},
            'account_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'fully_update': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'masteries': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'profile_icon': ('django.db.models.fields.IntegerField', [], {}),
            'region': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'runes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'summoner_id': ('django.db.models.fields.IntegerField', [], {}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 4, 0, 0)'}),
            'update_automatically': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'})
        },
        'lol.summonerrankedstatistics': {
            'Meta': {'object_name': 'SummonerRankedStatistics'},
            'assists': ('django.db.models.fields.IntegerField', [], {}),
            'champion_id': ('django.db.models.fields.IntegerField', [], {}),
            'damage_dealt': ('django.db.models.fields.IntegerField', [], {}),
            'damage_taken': ('django.db.models.fields.IntegerField', [], {}),
            'deaths': ('django.db.models.fields.IntegerField', [], {}),
            'double_kills': ('django.db.models.fields.IntegerField', [], {}),
            'gold': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'summoner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lol.Summoner']"}),
            'time_spent_dead': ('django.db.models.fields.IntegerField', [], {}),
            'triple_kills': ('django.db.models.fields.IntegerField', [], {}),
            'turrets_destroyed': ('django.db.models.fields.IntegerField', [], {}),
            'wins': ('django.db.models.fields.IntegerField', [], {})
        },
        'lol.summonerrating': {
            'Meta': {'unique_together': "(('summoner', 'game_map', 'game_mode'),)", 'object_name': 'SummonerRating'},
            'current_rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'game_map': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'game_mode': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leaves': ('django.db.models.fields.IntegerField', [], {}),
            'losses': ('django.db.models.fields.IntegerField', [], {}),
            'summoner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lol.Summoner']"}),
            'top_rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'wins': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['lol']
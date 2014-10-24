# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Player.rating'
        db.delete_column('lol_player', 'rating')

        # Adding field 'Player.tier'
        db.add_column('lol_player', 'tier',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Player.division'
        db.add_column('lol_player', 'division',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Player.rank'
        db.add_column('lol_player', 'rank',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'SummonerRating.top_rating'
        db.delete_column('lol_summonerrating', 'top_rating')

        # Deleting field 'SummonerRating.leaves'
        db.delete_column('lol_summonerrating', 'leaves')

        # Deleting field 'SummonerRating.current_rating'
        db.delete_column('lol_summonerrating', 'current_rating')

        # Adding field 'SummonerRating.league'
        db.add_column('lol_summonerrating', 'league',
                      self.gf('django.db.models.fields.CharField')(max_length=127, null=True, blank=True),
                      keep_default=False)

        # Adding field 'SummonerRating.tier'
        db.add_column('lol_summonerrating', 'tier',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SummonerRating.division'
        db.add_column('lol_summonerrating', 'division',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SummonerRating.rank'
        db.add_column('lol_summonerrating', 'rank',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SummonerRating.miniseries_target'
        db.add_column('lol_summonerrating', 'miniseries_target',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'SummonerRating.miniseries_wins'
        db.add_column('lol_summonerrating', 'miniseries_wins',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'SummonerRating.miniseries_losses'
        db.add_column('lol_summonerrating', 'miniseries_losses',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Player.rating'
        raise RuntimeError("Cannot reverse this migration. 'Player.rating' and its values cannot be restored.")
        # Deleting field 'Player.tier'
        db.delete_column('lol_player', 'tier')

        # Deleting field 'Player.division'
        db.delete_column('lol_player', 'division')

        # Deleting field 'Player.rank'
        db.delete_column('lol_player', 'rank')

        # Adding field 'SummonerRating.top_rating'
        db.add_column('lol_summonerrating', 'top_rating',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'SummonerRating.leaves'
        raise RuntimeError("Cannot reverse this migration. 'SummonerRating.leaves' and its values cannot be restored.")
        # Adding field 'SummonerRating.current_rating'
        db.add_column('lol_summonerrating', 'current_rating',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'SummonerRating.league'
        db.delete_column('lol_summonerrating', 'league')

        # Deleting field 'SummonerRating.tier'
        db.delete_column('lol_summonerrating', 'tier')

        # Deleting field 'SummonerRating.division'
        db.delete_column('lol_summonerrating', 'division')

        # Deleting field 'SummonerRating.rank'
        db.delete_column('lol_summonerrating', 'rank')

        # Deleting field 'SummonerRating.miniseries_target'
        db.delete_column('lol_summonerrating', 'miniseries_target')

        # Deleting field 'SummonerRating.miniseries_wins'
        db.delete_column('lol_summonerrating', 'miniseries_wins')

        # Deleting field 'SummonerRating.miniseries_losses'
        db.delete_column('lol_summonerrating', 'miniseries_losses')


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
            'division': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
            'rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sight_wards_bought_in_game': ('django.db.models.fields.IntegerField', [], {}),
            'skin_index': ('django.db.models.fields.IntegerField', [], {}),
            'skin_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'summoner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lol.Summoner']"}),
            'summoner_level': ('django.db.models.fields.IntegerField', [], {}),
            'summoner_spell1': ('django.db.models.fields.IntegerField', [], {}),
            'summoner_spell2': ('django.db.models.fields.IntegerField', [], {}),
            'team_objective': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tier': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
            'masteries': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'profile_icon': ('django.db.models.fields.IntegerField', [], {}),
            'region': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'runes': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'blank': 'True'}),
            'summoner_id': ('django.db.models.fields.IntegerField', [], {}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 2, 1, 0, 0)'}),
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
            'division': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'game_map': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'game_mode': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.CharField', [], {'max_length': '127', 'null': 'True', 'blank': 'True'}),
            'losses': ('django.db.models.fields.IntegerField', [], {}),
            'miniseries_losses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'miniseries_target': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'miniseries_wins': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'summoner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lol.Summoner']"}),
            'tier': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'wins': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['lol']
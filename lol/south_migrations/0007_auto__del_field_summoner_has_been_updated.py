# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field players on 'Game'
        db.delete_table('lol_game_players')

        # Deleting field 'Summoner.has_been_updated'
        db.delete_column('lol_summoner', 'has_been_updated')

        # Removing index on 'Summoner', fields ['name']
        # db.delete_index('lol_summoner', ['name'])


    def backwards(self, orm):
        # Adding index on 'Summoner', fields ['name']
        db.create_index('lol_summoner', ['name'])

        # Adding M2M table for field players on 'Game'
        db.create_table('lol_game_players', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('game', models.ForeignKey(orm['lol.game'], null=False)),
            ('player', models.ForeignKey(orm['lol.player'], null=False))
        ))
        db.create_unique('lol_game_players', ['game_id', 'player_id'])

        # Adding field 'Summoner.has_been_updated'
        db.add_column('lol_summoner', 'has_been_updated',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    models = {
        'lol.game': {
            'Meta': {'ordering': "['-time']", 'object_name': 'Game'},
            'blue_team_won': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fetched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'game_id': ('django.db.models.fields.IntegerField', [], {}),
            'game_map': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'game_mode': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'unfetched_players': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
        },
        'lol.player': {
            'Meta': {'ordering': "['game']", 'object_name': 'Player'},
            'afk': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assists': ('django.db.models.fields.IntegerField', [], {}),
            'blue_team': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'boosted_experience_earned': ('django.db.models.fields.IntegerField', [], {}),
            'boosted_ip_earned': ('django.db.models.fields.IntegerField', [], {}),
            'champion_id': ('django.db.models.fields.IntegerField', [], {}),
            'champion_level': ('django.db.models.fields.IntegerField', [], {}),
            'combat_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
            'node_neutralisation_assists': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nodes_captured': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nodes_neutralised': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'objective_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'objectives': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'physical_damage_dealt': ('django.db.models.fields.IntegerField', [], {}),
            'physical_damage_taken': ('django.db.models.fields.IntegerField', [], {}),
            'ping': ('django.db.models.fields.IntegerField', [], {}),
            'premade_size': ('django.db.models.fields.IntegerField', [], {}),
            'queue_length': ('django.db.models.fields.IntegerField', [], {}),
            'rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {}),
            'skin_index': ('django.db.models.fields.IntegerField', [], {}),
            'skin_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'summoner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lol.Summoner']"}),
            'summoner_level': ('django.db.models.fields.IntegerField', [], {}),
            'summoner_spell1': ('django.db.models.fields.IntegerField', [], {}),
            'summoner_spell2': ('django.db.models.fields.IntegerField', [], {}),
            'time_spent_dead': ('django.db.models.fields.IntegerField', [], {}),
            'total_healing_done': ('django.db.models.fields.IntegerField', [], {}),
            'total_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'turrets_destroyed': ('django.db.models.fields.IntegerField', [], {}),
            'victory_points': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'won': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'lol.summoner': {
            'Meta': {'object_name': 'Summoner'},
            'account_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'fully_update': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'profile_icon': ('django.db.models.fields.IntegerField', [], {}),
            'region': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'runes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'summoner_id': ('django.db.models.fields.IntegerField', [], {}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 16, 0, 0)'}),
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
            'Meta': {'object_name': 'SummonerRating'},
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
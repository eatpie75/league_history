from django import forms
from django.contrib import admin
from models import Player, Summoner, Game, SummonerRating


class PlayerForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(PlayerForm, self).__init__(*args, **kwargs)
		#self.fields['winner_tags'].widget=forms.SelectMultiple(attrs={'style':'height:250px'})
		if 'instance' in kwargs:
			self.fields['summoner'].queryset=Summoner.objects.filter(pk=kwargs['instance'].summoner.pk)
			self.fields['game'].queryset=Game.objects.filter(pk=kwargs['instance'].game.pk)
		else:
			self.fields['summoner'].queryset=Player.objects.none()
			self.fields['game'].queryset=Game.objects.none()


class PlayerAdmin(admin.ModelAdmin):
	#list_filter=('summoner',)
	list_display=('summoner',)
	list_filter=('summoner__update_automatically', 'game__fetched', 'game__game_map', 'game__game_mode')
	search_fields=('game__game_id',)
	form=PlayerForm


class SummonerAdmin(admin.ModelAdmin):
	list_display=('name', 'level', 'time_updated', 'update_automatically', 'fully_update')
	list_editable=('update_automatically', 'fully_update')
	list_filter=('region', 'update_automatically')
	search_fields=('summoner_id', 'account_id', 'name')


class GameAdmin(admin.ModelAdmin):
	list_display=('time', 'game_id', 'game_map', 'game_mode', 'fetched')
	list_editable=('fetched',)
	list_filter=('game_map', 'game_mode', 'fetched')
	search_fields=('game_id', 'unfetched_players')


class SummonerRatingAdmin(admin.ModelAdmin):
	list_display=('summoner', 'game_map', 'game_mode', 'current_rating', 'wins', 'losses')
	list_filter=('summoner__region', 'game_map', 'game_mode')
	search_fields=('summoner__name',)
	#form=GameForm


admin.site.register(Player, PlayerAdmin)
admin.site.register(Summoner, SummonerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(SummonerRating, SummonerRatingAdmin)

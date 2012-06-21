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
	list_filter=('summoner__update_automatically', 'game__fetched')
	search_fields=('game__game_id',)
	form=PlayerForm


class SummonerAdmin(admin.ModelAdmin):
	list_display=('name', 'level', 'time_updated', 'update_automatically', 'fully_update')
	list_editable=('update_automatically', 'fully_update')
	list_filter=('region',)
	search_fields=('summoner_id', 'account_id', 'name')


class GameForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(GameForm, self).__init__(*args, **kwargs)
		#self.fields['winner_tags'].widget=forms.SelectMultiple(attrs={'style':'height:250px'})
		if 'instance' in kwargs:
			self.fields['players'].queryset=kwargs['instance'].players.all()
		else:
			self.fields['players'].queryset=Player.objects.none()
		# if 'instance' in kwargs:
		# 	if kwargs['instance'].series and kwargs['instance'].series.winner and kwargs['instance'].series.loser:
		# 		self.fields['series'].queryset=Series.objects.filter(Q(winner=kwargs['instance'].series.winner)|Q(loser=kwargs['instance'].series.loser)).select_related()
		# 		self.fields['winner'].queryset=Player.objects.filter(Q(id=kwargs['instance'].series.winner.id)|Q(id=kwargs['instance'].series.loser.id)).select_related()
		# 		self.fields['loser'].queryset=Player.objects.filter(Q(id=kwargs['instance'].series.winner.id)|Q(id=kwargs['instance'].series.loser.id)).select_related()
		# 		self.fields['set'].initial=Match.objects.filter(series=kwargs['instance'].series).count()+1
		# 	elif kwargs['instance'].winner and kwargs['instance'].loser:
		# 		self.fields['series'].queryset=Series.objects.filter(Q(winner=kwargs['instance'].winner)|Q(loser=kwargs['instance'].loser)).select_related()


class GameAdmin(admin.ModelAdmin):
	list_display=('game_id', 'fetched')
	list_editable=('fetched',)
	list_filter=('game_map', 'game_mode')
	search_fields=('game_id',)
	form=GameForm


class SummonerRatingAdmin(admin.ModelAdmin):
	list_display=('summoner', 'game_map', 'game_mode', 'current_rating', 'wins', 'losses')
	list_filter=('summoner__region', 'game_map', 'game_mode')
	search_fields=('summoner__name',)
	#form=GameForm


admin.site.register(Player, PlayerAdmin)
admin.site.register(Summoner, SummonerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(SummonerRating, SummonerRatingAdmin)

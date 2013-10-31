from django import forms
from django.contrib import admin
from models import Player, Summoner, Game, SummonerRating
from tasks import summoner_auto_task, fill_game


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
	list_display=('summoner', 'game_time', 'tier', 'division', 'rank', 'rank_to_number', 'game_link')
	list_filter=('summoner__update_automatically', 'game__fetched', 'game__game_map', 'game__game_mode', 'leaver', 'won')
	list_per_page=25
	search_fields=('game__game_id', 'summoner__name')
	form=PlayerForm

	def game_time(self, obj):
		return obj.game.time

	def rank_to_number(self, obj):
		return obj.rank_to_number

	def game_link(self, obj):
		return "<a href='{}'>Link</a>".format(obj.get_absolute_url())
	game_link.short_description='Link'
	game_link.allow_tags=True


class SummonerAdmin(admin.ModelAdmin):
	list_display=('name', 'level', 'time_updated', 'profile_icon', 'update_automatically', 'fully_update', 'summoner_link')
	list_editable=('update_automatically', 'fully_update')
	list_filter=('region', 'update_automatically')
	search_fields=('summoner_id', 'account_id', 'name')
	actions=['force_update']

	def force_update(self, request, qs):
		summoners_updated=len(qs)
		for summoner in qs:
			summoner_auto_task.apply_async(args=[summoner.pk,])
		if summoners_updated==1:
			message='1 summoner was'
		else:
			message='{} summoners were'.format(summoners_updated)
		self.message_user(request, '{} added to the update queue.'.format(message))
	force_update.short_description='Add selected summoners to update queue'

	def summoner_link(self, obj):
		return "<a href='{}'>Link</a>".format(obj.get_absolute_url())
	summoner_link.short_description='Link'
	summoner_link.allow_tags=True


class GameAdmin(admin.ModelAdmin):
	list_display=('time', 'game_id', 'game_map', 'game_mode', 'fetched', 'game_link')
	list_editable=('fetched',)
	list_filter=('region', 'game_map', 'game_mode', 'fetched', 'time')
	search_fields=('game_id', 'unfetched_players')
	actions=['force_fill']

	def force_fill(self, request, qs):
		games_filled=len(qs)
		for game in qs:
			fill_game.apply_async(args=[game.pk,])
		if games_filled==1:
			message='1 game was'
		else:
			message='{} games were'.format(games_filled)
		self.message_user(request, '{} added to the fill queue.'.format(message))
	force_fill.short_description='Add selected games to fill queue'

	def game_link(self, obj):
		return "<a href='{}'>Link</a>".format(obj.get_absolute_url())
	game_link.short_description='Link'
	game_link.allow_tags=True


class SummonerRatingForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(SummonerRatingForm, self).__init__(*args, **kwargs)
		#self.fields['winner_tags'].widget=forms.SelectMultiple(attrs={'style':'height:250px'})
		if 'instance' in kwargs:
			self.fields['summoner'].queryset=Summoner.objects.filter(pk=kwargs['instance'].summoner.pk)
		else:
			self.fields['summoner'].queryset=Player.objects.none()


class SummonerRatingAdmin(admin.ModelAdmin):
	list_display=('summoner', 'game_map', 'game_mode', 'tier', 'division', 'rank', 'wins', 'losses', 'update_automatically', 'fully_update', 'summoner_link')
	# list_editable=('summoner__update_automatically', 'summoner__fully_update')
	list_filter=('summoner__region', 'game_map', 'game_mode', 'tier')
	search_fields=('summoner__name',)
	form=SummonerRatingForm

	def update_automatically(self, obj):
		return obj.summoner.update_automatically
	update_automatically.short_description='Auto Update'

	def fully_update(self, obj):
		return obj.summoner.fully_update
	fully_update.short_description='Auto Fill'

	def summoner_link(self, obj):
		return "<a href='{}'>Link</a>".format(obj.summoner.get_absolute_url())
	summoner_link.short_description='Link'
	summoner_link.allow_tags=True


admin.site.register(Player, PlayerAdmin)
admin.site.register(Summoner, SummonerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(SummonerRating, SummonerRatingAdmin)

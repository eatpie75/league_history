from django.contrib import admin
from models import Player, Summoner, Game, UnknownPlayer


class PlayerAdmin(admin.ModelAdmin):
	#list_filter=('game',)
	search_fields=('game__game_id',)


class UnknownPlayerAdmin(admin.ModelAdmin):
	search_fields=('summoner_id',)


class GameAdmin(admin.ModelAdmin):
	list_display=('game_id', 'time_display')
	search_fields=('game_id',)

admin.site.register(Player, PlayerAdmin)
admin.site.register(Summoner)
admin.site.register(Game, GameAdmin)
admin.site.register(UnknownPlayer, UnknownPlayerAdmin)

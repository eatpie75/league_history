from django.contrib import admin
from models import Player, Summoner, Game, UnknownPlayer

class PlayerAdmin(admin.ModelAdmin):
	list_filter=('game',)

class GameAdmin(admin.ModelAdmin):
	search_fields=('game_id',)

admin.site.register(Player, PlayerAdmin)
admin.site.register(Summoner)
admin.site.register(Game, GameAdmin)
admin.site.register(UnknownPlayer)
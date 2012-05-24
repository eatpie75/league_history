from django.contrib import admin
from models import Game


class GameAdmin(admin.ModelAdmin):
	list_display=('game_id', 'updated')
	search_fields=('game_id',)

admin.site.register(Game, GameAdmin)

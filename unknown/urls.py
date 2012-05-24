from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns=patterns('unknown.lol.views',
	url(r'^game/(NA|EUW|EUNE)/(\d{1,12})/$', 'view_game', name='view_game'),
	url(r'^game/$', 'game_list', name='game_list'),
	url(r'^summoner/(NA|EUW|EUNE)/(\d{1,12})/([-\w]*?)/games/', 'view_summoner_games', name='view_summoner_games'),
	url(r'^summoner/(NA|EUW|EUNE)/(\d{1,12})/([-\w]*?)/champions/(\d{1,12})/([-\w])*/', 'view_summoner_specific_champion', name='view_summoner_specific_champion'),
	url(r'^summoner/(NA|EUW|EUNE)/(\d{1,12})/([-\w]*?)/champions/', 'view_summoner_champions', name='view_summoner_champions'),
	url(r'^summoner/(NA|EUW|EUNE)/(\d{1,12})/([-\w]*?)/', 'view_summoner', name='view_summoner'),
	url(r'^search/([-\w\s]*)/', 'search', name='search'),
	url(r'^run_auto/$', 'run_auto'),

	# Uncomment the admin/doc line below to enable admin documentation:
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)
urlpatterns+=patterns('unknown.lol.ajax',
	url(r'^ajax/player_info/(\d{1,12})/$', 'player_info', name='ajax_player_info'),
)

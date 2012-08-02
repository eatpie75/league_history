from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns=patterns('lol.views',
	url(r'^game/(?P<region>NA|EUW|EUNE)/(?P<game_id>\d{1,12})/$', 'view_game', name='view_game'),
	url(r'^game/$', 'game_list', name='game_list'),
	url(r'^summoner/(?P<region>NA|EUW|EUNE)/(?P<account_id>\d{1,12})/(?P<slug>[-\w]*?)/games/', 'view_summoner_games', name='view_summoner_games'),
	url(r'^summoner/(?P<region>NA|EUW|EUNE)/(?P<account_id>\d{1,12})/(?P<slug>[-\w]*?)/champions/(?P<champion_id>\d{1,12})/(?P<champion_slug>[-\w])*/', 'view_summoner_specific_champion', name='view_summoner_specific_champion'),
	url(r'^summoner/(?P<region>NA|EUW|EUNE)/(?P<account_id>\d{1,12})/(?P<slug>[-\w]*?)/champions/', 'view_summoner_champions', name='view_summoner_champions'),
	url(r'^summoner/(?P<region>NA|EUW|EUNE)/(?P<account_id>\d{1,12})/(?P<slug>[-\w]*?)/', 'view_summoner', name='view_summoner'),
	url(r'^champions/(?P<champion_id>\d{1,12})/(?P<champion_slug>[-\w]*?)/$', 'view_champion', name='view_champion'),
	url(r'^champions/$', 'view_all_champions', name='view_all_champions'),
	url(r'^search/([-\w\s]*)/$', 'search', name='search'),
	url(r'^run_auto/$', 'run_auto'),

	url(r'^admin/status/', 'client_status'),

	# Uncomment the admin/doc line below to enable admin documentation:
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)
urlpatterns+=patterns('lol.ajax',
	url(r'^ajax/player_info/(\d{1,12})/$', 'player_info', name='ajax_player_info'),
	url(r'^ajax/summoner_games/(?P<region>0|1|2)/(?P<account_id>\d{1,12})/$', 'summoner_games', name='ajax_summoner_games'),
	url(r'^ajax/force_update/(?P<region>0|1|2)/(?P<account_id>\d{1,12})/$', 'force_update', name='ajax_force_update'),
	url(r'^ajax/force_update_status/(?P<region>0|1|2)/(?P<account_id>\d{1,12})/$', 'force_update_status', name='ajax_force_update_status'),
)
# urlpatterns+=patterns('', url(r'^redis/status/', include('redis_cache.stats.urls', namespace='redis_cache')))

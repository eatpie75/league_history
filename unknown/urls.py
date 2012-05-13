from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns=patterns('unknown.main.views',
	url(r'^game/(\d{1,12})/$', 'view_game', name='view_game'),
	url(r'^game/$', 'game_list', name='game_list'),
	url(r'^summoner/(\d{1,12})/([-\w])*/', 'view_summoner', name='view_summoner'),

	# Uncomment the admin/doc line below to enable admin documentation:
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)
urlpatterns+=patterns('unknown.main.ajax',
	url(r'^ajax/player_info/(\d{1,12})/$', 'player_info', name='ajax_player_info'),
)

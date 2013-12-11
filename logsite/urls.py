from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'logsite.views.home', name='home'),
	# url(r'^logsite/', include('logsite.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
	#url(r'^$', 'logapp.views.index'),
	url(r'^$', 'logapp.views.chronological'),
	url(r'^chronological/$', 'logapp.views.chronological'),
	url(r'^text/$', 'logapp.views.text_search'),
	url(r'^user/$', 'logapp.views.user_search'),
	url(r'^statistics/$', 'logapp.views.statistics'),
	url(r'^streams/$', 'logapp.views.streams'),
	url(r'^streams/data.*', 'logapp.views.streamsdata'),
	url(r'^sql/$', 'logapp.views.sql'),
	url(r'^streams/time.*', 'logapp.views.time'),
	url(r'^robots.txt$', 'logapp.views.robots'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
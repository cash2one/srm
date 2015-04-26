# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-


from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'apps.dashboard.views.homepage', name='home'),
    url(r'^dashboard/$', 'apps.dashboard.views.homepage', name='home'),
    url(r'^dashboard/$', 'apps.dashboard.views.homepage', name='home'),
    url(r'^websites/$', 'apps.websites.views.homepage', name='home'),
    url(r'^settings/$', 'apps.settings.views.homepage', name='home'),


    # Examples:
    # url(r'^$', 'srm.views.home', name='home'),
    # url(r'^srm/', include('srm.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

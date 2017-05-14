"""
Definition of urls for DjangoWebProject2.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
from django.conf.urls import include
from django.contrib import admin

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^quotes', app.views.quotes, name='quotes'),
    url(r'^about', app.views.about, name='about'),
    url(r'^myprofile$', app.views.myprofile, name='myprofile'),
    url(r'^myprofile/(quotes|poetry|stories)', app.views.loadData),
    url(r'^write!/$', app.views.write, name='write!'),
    url(r'^poetry', app.views.poetry, name='poetry'),
    url(r'^shortstories', app.views.shortStories, name='shortstories'),
    url(r'^profile_search', app.views.profileSearch, name='pSearch'),
    url(r'^quotes', app.views.quotes, name='quotes'),
    url(r'^look/(quote|poetry|story)/([0-9]*)$', app.views.look), #name is redundant on some of those
    url(r'^look/(quote|poetry|story)/([0-9]*)/upvote', app.views.upvote),
    url(r'^register/$', app.views.register, name='register'),
    url(r'^login/$', app.views.mylogin, name='mylogin'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
]

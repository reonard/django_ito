__author__ = 'reonard'
from django.conf.urls import url

from django.contrib import admin
from django.contrib.auth.views import login, logout

from app.ticketmgr.views import index, create_incident, show_ticket, update_incident, create_action
from app.comm.views import get_terminal_info, error_no_perm, get_owner


urlpatterns = [
    url(r'^user_hint/$', get_owner),
    url(r'^get_terminal_info/$', get_terminal_info),
    url(r'^index/$', index, name='index'),
    url(r'^detail/([0-9]+)/$', show_ticket, name='show_ticket'),
    url(r'^create_incident/$', create_incident, name='create_incident'),
    url(r'^update_incident/([0-9]+)/$', update_incident, name='update_incident'),
    url(r'^create_action/([0-9]+)/$', create_action, name='create_action'),
]
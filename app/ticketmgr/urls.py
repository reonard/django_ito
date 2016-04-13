__author__ = 'reonard'
from django.conf.urls import url

from app.ticketmgr.views import index, create_incident, show_ticket, update_incident, create_action, ajax_incident_list
from app.comm.views import get_terminal_info, get_owner, get_maintainer


urlpatterns = [
    url(r'^user_hint/$', get_owner),
    url(r'^get_maintainer/$', get_maintainer),
    url(r'^get_terminal_info/$', get_terminal_info),
    url(r'^get_incident_list/$', ajax_incident_list),
    url(r'^index/$', index, name='index'),
    url(r'^detail/([0-9]+)/$', show_ticket, name='show_ticket'),
    url(r'^create_incident/$', create_incident, name='create_incident'),
    url(r'^update_incident/([0-9]+)/$', update_incident, name='update_incident'),
    url(r'^create_action/([0-9]+)/$', create_action, name='create_action'),
]
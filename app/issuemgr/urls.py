__author__ = 'reonard'
from django.conf.urls import url


from app.issuemgr.views import index, ajax_problem_index, create_problem, create_action, update_problem, show_ticket

urlpatterns = [
    url(r'^index/$', index, name='index'),
    url(r'^get_problem_list', ajax_problem_index),
    url(r'^detail/([0-9]+)/$', show_ticket, name='show_ticket'),
    url(r'^create_problem/$', create_problem, name='create_problem'),
    url(r'^update_problem/([0-9]+)/$', update_problem, name='update_problem'),
    url(r'^create_action/([0-9]+)/$', create_action, name='create_action'),
]
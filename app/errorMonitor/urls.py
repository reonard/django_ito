__author__ = 'reonard'
from django.conf.urls import url


from app.errorMonitor.views import index, ajax_error_index
from app.comm.views import get_terminal_info, error_no_perm, get_owner


urlpatterns = [
    url(r'^index/$', index, name='index'),
    url(r'^error_list', ajax_error_index)

]
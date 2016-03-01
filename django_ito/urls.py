"""django_ito URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout

from app.ticketmgr.views import index, create_incident, show_ticket, update_incident, create_action
from app.comm.views import get_terminal_info, error_no_perm, get_owner


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/', login, {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout/', logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^ticketmgr/user_hint/$', get_owner),
    url(r'^ticketmgr/get_terminal_info/$', get_terminal_info),
    url(r'^user_hint/$', get_owner),
    url(r'^ticketmgr/index/$', index, name='index'),
    url(r'^ticketmgr/detail/([0-9]+)/$', show_ticket, name='show_ticket'),
    url(r'^ticketmgr/create_incident/$', create_incident, name='create_incident'),
    url(r'^ticketmgr/update_incident/([0-9]+)/$', update_incident, name='update_incident'),
    url(r'^ticketmgr/create_action/([0-9]+)/$', create_action, name='create_action'),
    url(r'^error_no_perm/$', error_no_perm)
]

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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from app.comm.views import error_no_perm, get_owner


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/', login, {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout/', logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^user_hint/$', get_owner),
    url(r'^error_no_perm/$', error_no_perm),
    url(r'^ticketmgr/', include('app.ticketmgr.urls', namespace='ticketmgr')),
    url(r'^errormonitor/', include('app.errorMonitor.urls', namespace='errormonitor')),
    url(r'^issuemgr/', include('app.issuemgr.urls', namespace='issuemgr')),
]

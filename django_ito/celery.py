# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import Celery
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ito.settings')
from django.conf import settings


app = Celery('django_ito')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))




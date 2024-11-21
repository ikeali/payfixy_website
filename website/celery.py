# from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

app = Celery('website')
app.config_from_object('django.conf:settings', namespace='CELERY')


# Discover tasks from installed apps
app.autodiscover_tasks()

# app.conf.broker_url = config('CELERY_BROKER_URL')
app.conf.result_backend = 'redis://localhost:6379/0'  # Example for Redis



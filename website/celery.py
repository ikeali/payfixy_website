# from __future__ import absolute_import, unicode_literals
import os

from django.conf import settings

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

app = Celery('website')
app.config_from_object('django.conf:settings', namespace='CELERY')
# app.config_from_object(f'django.conf:{settings.__name__}', namespace='CELERY')



# Discover tasks from installed apps
app.autodiscover_tasks()

# app.conf.broker_url = config('CELERY_BROKER_URL')
app.conf.result_backend = 'redis://localhost:6379/0'



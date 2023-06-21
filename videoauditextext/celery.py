
from __future__ import absolute_import
import os
from django.conf import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoauditextext.settings')

celery_app = Celery('videoauditextext')
celery_app.config_from_object(settings, namespace='CELERY')
celery_app.autodiscover_tasks()

@celery_app.task(bind=True)
def hello():
    print ("This task is registering successfully")
    
    

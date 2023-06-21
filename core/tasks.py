
from celery import shared_task
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings
import os

@shared_task
def clean_media():
    folder = os.listdir(settings.MEDIA_ROOT)
    for file in folder:
        file_path = os.path.join(settings.MEDIA_ROOT, file)
        creation_time = os.path.getctime(file_path)
        creation_datetime = datetime.fromtimestamp(creation_time)
        now = datetime.now()
        delta = relativedelta(now,creation_datetime)
        if delta.minutes >= 10:
            print('Cleaning trash media files...')
            os.remove(file_path)
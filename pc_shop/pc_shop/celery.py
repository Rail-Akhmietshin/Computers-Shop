import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pc_shop.settings")

app = Celery("pc_shop")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
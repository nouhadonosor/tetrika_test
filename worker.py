import os

from celery import Celery

from config import settings


celery_app = Celery("worker", include=["tasks"])

celery_app.conf.broker_url = settings.celery_broker_url

celery_app.conf.result_backend = settings.celery_result_backend

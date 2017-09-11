from celery import Celery

import settings

app = Celery('tasks', include=[
    'bidong.task.workers', ])

app.conf.update(
    broker_url=settings.celery['broker'],
    timezone='Asia/Shanghai',
    enable_utc=True
)

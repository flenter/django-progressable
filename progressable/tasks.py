from celery.task import PeriodicTask
from datetime import timedelta, datetime


class ProgressableCleanupTask(PeriodicTask):
    run_every = timedelta(minutes=10)

    def run(self, *args, **kwargs):
        from .models import TaskStatus
        from django.conf import settings

        expires = settings.CELERY_TASK_RESULT_EXPIRES
        youngest = datetime.now() - timedelta(seconds=expires)

        stati = TaskStatus.objects.zfilter(publish_date__lte=youngest)
        for status in stati:
            status.delete()

from django.utils.translation import ugettext_lazy as _

from admin_tools.dashboard.modules import DashboardModule


class TaskStatusModule(DashboardModule):
    title = _('Links')
    template = 'progressable/dashboard/modules/task_list.html'
    layout = 'stacked'

    def __init__(self, *args, **kwargs):
        super(TaskStatusModule, self).__init__(*args, **kwargs)

        #print dir(self)
        self.css_classes.append("tscm_task_status")

    def init_with_context(self, context):
        from django.contrib.sites.models import Site
        from django.conf import settings

        from progressable.models import TaskStatus
        from datetime import timedelta, datetime

        expires = settings.CELERY_TASK_RESULT_EXPIRES
        youngest = datetime.now() - timedelta(seconds=expires)

        site = Site.objects.get_current().domain

        tasks = TaskStatus.objects.order('-publish_date')

        filtered_tasks = []

        for task in tasks:
            if (
                    task.site == site and
                    task.hidden == False and
                    task.publish_date > youngest
                ):
                filtered_tasks.append(task)

        filtered_tasks = filtered_tasks[:10]
        self.children = filtered_tasks

    def is_empty():
        return False


class RedisStatusModule(DashboardModule):
    title = _('Redis status')
    template = 'progressable/dashboard/modules/redis_status.html'
    layout = 'stacked'

    def init_with_context(self, context):
        from redis import Redis

        db = Redis()

        self.children = [db.info()]

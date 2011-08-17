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
        from progressable.models import TaskStatus

        from datetime import timedelta, datetime
        from django.conf import settings

        youngest = datetime.now() - timedelta(seconds= settings.CELERY_TASK_RESULT_EXPIRES)

        tasks = TaskStatus.objects.order('-publish_date').zfilter(publish_date__gt = youngest).exclude(hidden=True)

        self.children = tasks

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


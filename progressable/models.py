from celery.states import EXCEPTION_STATES, READY_STATES
from redisco import models

from progressable.fields import UUIDField
<<<<<<< HEAD
from progressable.states import PROGRESS

class TaskStatus(models.Model):
    staff_required = models.BooleanField(default=True)
    hidden = models.BooleanField(default=False)
    uid = UUIDField()
    task_id = models.CharField()
    publish_date = models.DateTimeField(auto_now_add = True, indexed=True)
    task_name = models.CharField(max_length = 1000)
    title = models.CharField()
    _result = None

    def __unicode__(self):
        if self.title:
            return unicode(self.title)
        elif self.task_name:
            return unicode(self.task_name)
        else:
            return u"undefined name"

    def get_result(self):
        if not self._result:
            from celery.utils import get_cls_by_name
            Task = get_cls_by_name(self.task_name)
            self._result = Task.AsyncResult(self.task_id)
        return self._result

    @property
    def status(self):
        return self.get_result().status

    @property
    def percentage(self):
        result = self.get_result()
        if result.ready():
            return 100
        if result.state == PROGRESS:
            return result.info.get('completed', -1)
        return -1

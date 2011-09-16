from redisco import models

from progressable.fields import UUIDField#, UUIDField2
from progressable.states import PROGRESS

class TaskStatusMixin(object):
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

class TaskStatus(models.Model, TaskStatusMixin):
    staff_required = models.BooleanField(default=True)
    hidden = models.BooleanField(default=False)
    uid = UUIDField()
    task_id = models.CharField()
    publish_date = models.DateTimeField(auto_now_add = True, indexed=True)
    task_name = models.CharField(max_length = 1000)
    title = models.CharField()
    site = models.CharField()
    _result = None


# small test for stdnet support. Unfortunately stdnet didn't seem to really support 
# complex enough queries (such as filtering on datetime)
#from stdnet import orm
#from datetime import datetime
#class TaskStatus2(orm.StdModel, TaskStatusMixin):
#    staff_required = orm.BooleanField(default=True)
#    hidden = orm.BooleanField(default=True)
#    uid = UUIDField2()
#    task_name = orm.SymbolField()
#    title = orm.SymbolField()
#    task_id = orm.SymbolField()
#    publish_date = orm.DateTimeField(default=datetime.now, index=True)
#    _result = None
#
#orm.register(TaskStatus2, 'redis://localhost:6379/?db=13')

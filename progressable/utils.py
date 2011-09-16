from progressable.models import TaskStatus as TaskStatus
from progressable.states import PROGRESS

def register_task(result, staff_required = False, hidden = True, title=''):
    
    from django.contrib.sites.models import Site

    t_status = TaskStatus(
        staff_required = staff_required,
        task_id = result.task_id,
        hidden = hidden, 
        task_name = result.task_name,
        title=title,
        site = Site.objects.get_current().domain
    )

    t_status.save()

    return t_status

class ProgressTaskMixin():
    def update_progress(self, percentage):
        self.update_state(
                state = PROGRESS,
                meta = {'completed': percentage}
                )


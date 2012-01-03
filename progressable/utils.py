from progressable.models import TaskStatus as TaskStatus
from progressable.states import PROGRESS

def register_task(result, staff_required = False, hidden = True, title='', site="CURRENT"):

    from django.contrib.sites.models import Site

    if site == "CURRENT":
        site_reference = Site.objects.get_current().domain
    else:
        site_reference = site.domain
    print hidden, site_reference, type(site_reference)
    t_status = TaskStatus(
        staff_required = staff_required,
        task_id = result.task_id,
        hidden = hidden, 
        task_name = result.task_name,
        title=title,
        site=site_reference
    )

    t_status.save()

    print len(TaskStatus.objects.all())

    return t_status


class ProgressTaskMixin():
    def update_progress(self, percentage):
        self.update_state(
                state = PROGRESS,
                meta = {'completed': percentage}
                )

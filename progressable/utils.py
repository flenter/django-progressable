#import uuid
#import uuid

from progressable.models import TaskStatus

def register_task(result, staff_required = False, hidden = True, title=''):

    t_status = TaskStatus(
        staff_required = staff_required,
        task_id = result.task_id,
        hidden = hidden, 
        task_name = result.task_name,
        title=title
    )

    return t_status

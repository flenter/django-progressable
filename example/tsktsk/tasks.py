from celery.task import task

from time import sleep

from progressable.states import PROGRESS

@task
def add(x,y):

    for i in range(100):
        add.update_state(state=PROGRESS,
            meta={"completed":i})
        sleep(1)

    return x + y



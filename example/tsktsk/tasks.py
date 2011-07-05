from celery.task import task

from time import sleep

<<<<<<< HEAD
from progressable.states import PROGRESS

=======
>>>>>>> e36da1902b017aede1bb1b38288b7dd4bd401156
@task
def add(x,y):

    for i in range(100):
<<<<<<< HEAD
        add.update_state(state=PROGRESS,
=======
        add.update_state(state="PROGRESS",
>>>>>>> e36da1902b017aede1bb1b38288b7dd4bd401156
            meta={"completed":i})
        sleep(1)

    return x + y



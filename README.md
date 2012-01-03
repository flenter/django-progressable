Introduction
============

Create tasks that can show up in the admin interface. It relies on a couple of things:
* redis (installed and running). 
* django-admin-tools (for displaying content in the admin)
* django-celery
* tastypie (for supplying task information via a RESTful api)

See the example project for an example implementation.


Installation
------------

clone the repository and run the ``setup.py``:

    git clone git@github.com:flenter/django-progressable.git
    cd django-progressable
    python setup.py install


### How to use this?

To try the example, go to the example project folder and run:

    pip install -r conf/requirements.txt

and (assuming the example project will be run via manage.py runserver):

    pip install -r conf/dev_requirements.txt

After that the usual two commands:

    python manage.py syncdb
    python manage.py migrate


Or check two files from the example project.

* `tsktsk/views.py` here some task are created with their corresponding TaskStatus objects
* `tsktsk/tasks.py` contains a task that updates itself on its progress
* `dashboard.py` This is a custom dashboard that includes the 'Task Status Information' 
and 'Redis status information' module



For people who just want to know how to implement 'progressable' quick'n'dirty, here's a short howto:

1. make sure you have set up django and celery with redis. Set the CELERY_TASK_RESULT_EXPIRES variable in your settings. This is the timeout for the information in Redis.
2. make sure you register your task by calling register_task(celery_task_instance, staff_required = True, hidden = False) will make sure it will be visible in the admin (the register_task can be found in progressable.utils namespace).
3. update your task to update it's progress info as a status update. 

Note: This continuous updating is why I've chosen for a Redis/Redisco implementation. The idea here is that tasks update themselves often, a scenario that doesn't look to be ideal for the traditional database.


#### A sample implementation of a task:

    from celery.task import task
    from time import sleep
    from progressable.states import PROGRESS

    @task
    def add(x, y):
      for i in range(100):
        add.update_status(
            state = "PROGRESS",
            meta={'completed':i}
        )

      return x + y


#### On a final note:

* the current implementation is not suited for running multiple sites on the same redis db. In fact there's little control over which db etc the information is stored
 * The jquery code for the django-admin is inline, this should be done more 
  nicely
* the admin module is not really multi-langual yet (and might never fully be because the title of a taskstatus object is generated when it is created ).



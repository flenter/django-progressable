from progressable.api import TaskStatusResource
#from progressable import api

#tsr = api.TaskStatusResource()

#print tsr.urls

status_resource = TaskStatusResource()

from django.conf.urls.defaults import patterns, url, include


urlpatterns = patterns('',
        url(r'', include(status_resource.urls)),)

#status_resource.urls.patterns

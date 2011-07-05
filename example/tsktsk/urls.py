from django.conf.urls.defaults import patterns

from tsktsk.views import StartTaskView


urlpatterns = patterns('',
    (r'$', StartTaskView.as_view()),
)

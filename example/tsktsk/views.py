# Create your views here.
from django.views.generic import TemplateView

class StartTaskView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        from tsktsk.tasks import add

        result = add.delay(10, 10)#,], expires=60*60)

        from progressable.utils import register_task

        t = register_task(result, title = "Test task (not hidden)", hidden=False)
        t.save()

        t = register_task(result, title = "Test task (hidden)", hidden=True)
        t.save()


        from django.contrib.sites.models import Site

        t = register_task(result, title="Tesk task (not for this site)", hidden=False, site=Site.objects.get(pk=2))

        print t.uid, t.id

        context = super(StartTaskView, self).get_context_data(**kwargs)
        return context

# Create your views here.
from django.views.generic import TemplateView

class StartTaskView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        from tsktsk.tasks import add

        result = add.delay(10, 10)#,], expires=60*60)

        from progressable.utils import register_task

        t = register_task(result, title = "Test task", hidden=False)
        t.save()
        print t.uid, t.id

        context = super(StartTaskView, self).get_context_data(**kwargs)
        return context

# Create your views here.
from django.views.generic import TemplateView


class StartTaskView(TemplateView):
    template_name = "index.html"

    def create_task(self, hidden=False, site="DEFAULT"):

        from tsktsk.tasks import add
        from progressable.utils import register_task

        result = add.delay(10, 10)

        if site == "DEFAULT":
            t = register_task(
                    result,
                    title="Test task (hidden == %s)" % hidden,
                    hidden=hidden
                )
        else:

            title = "Test task (hidden == %s) for site %s" % (hidden, site)
            t = register_task(
                    result,
                    title=title,
                    hidden=hidden,
                    site=site
                )

        t.save()

        return t

    def get_context_data(self, **kwargs):

        from django.contrib.sites.models import Site

        self.create_task(hidden=False)
        self.create_task(hidden=True)
        self.create_task(hidden=False, site=Site.objects.get(pk=2))

        context = super(StartTaskView, self).get_context_data(**kwargs)
        return context

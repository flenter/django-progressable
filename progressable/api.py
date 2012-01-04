from tastypie.resources import Resource

from tastypie import fields
from tastypie.bundle import Bundle

from progressable.models import TaskStatus


class TaskStatusResource(Resource):
    title = fields.CharField(attribute="title")
    status = fields.CharField(attribute="status")
    percentage = fields.FloatField(attribute="percentage")

    class Meta:
        resource_name = 'task_status'
        object_class = TaskStatus

    def get_resource_uri(self, bundle_or_obj):

        kwargs = {
            'resource_name': self._meta.resource_name,
        }

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.uid
        else:
            kwargs['pk'] = bundle_or_obj.uid

        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name

        return self._build_reverse_url("api_dispatch_detail", kwargs=kwargs)

    def obj_get(self, request=None, **kwargs):

        try:
            return self._meta.object_class.objects.filter(uid=kwargs['pk'])[0]

        except IndexError:

            from tastypie.exceptions import NotFound

            raise NotFound("Sorry, not found.")

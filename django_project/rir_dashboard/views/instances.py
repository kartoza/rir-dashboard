from django.views.generic.base import TemplateView
from rir_data.models.instance import Instance


class InstancesView(TemplateView):
    template_name = 'pages/instances.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instances'] = Instance.objects.all()
        return context

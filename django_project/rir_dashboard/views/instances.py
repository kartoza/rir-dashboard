from django.views.generic.base import TemplateView


class InstancesView(TemplateView):
    template_name = 'pages/instances.html'
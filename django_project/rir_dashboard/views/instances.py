from django.views.generic.base import TemplateView
from rir_data.models.instance import Instance, InstanceCategory


class InstancesView(TemplateView):
    template_name = 'pages/instances.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance_categories = {}
        for category in InstanceCategory.objects.all().order_by('order'):
            instance_categories[category.name] = category.instance_set.order_by('name')

        other_instance = Instance.objects.filter(category__isnull=True)
        if other_instance.count() > 0:
            instance_categories['Others'] = Instance.objects.filter(category__isnull=True)

        context['instance_categories'] = instance_categories
        return context

from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from rir_data.models.instance import Instance


class BaseDashboardView(TemplateView):
    instance = None

    def get_context_data(self, **kwargs):
        self.instance = get_object_or_404(
            Instance, slug=kwargs.get('slug', '')
        )

        context = super().get_context_data(**kwargs)
        context.update(self.context_view)
        context['dashboard_title'] = self.dashboard_title
        context['instance'] = self.instance
        return context

    @property
    def dashboard_title(self):
        raise NotImplementedError

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        return {}

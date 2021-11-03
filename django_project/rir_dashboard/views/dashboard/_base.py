from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from rir_data.models.instance import Instance


class BaseDashboardView(View):
    instance = None
    template_name = ''

    def get_context_data(self, **kwargs):
        self.instance = get_object_or_404(
            Instance, slug=kwargs.get('slug', '')
        )
        context = {}
        context.update(self.context_view)
        context['dashboard_title'] = self.dashboard_title
        context['page_title'] = 'Dashboard'
        context['instance'] = self.instance
        return context

    def get(self, request, **kwargs):
        return render(
            request, self.template_name, self.get_context_data(**kwargs)
        )

    @property
    def dashboard_title(self):
        raise NotImplementedError

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        return {}

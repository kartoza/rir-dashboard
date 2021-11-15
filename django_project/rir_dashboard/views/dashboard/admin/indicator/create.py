from django.http import Http404
from django.shortcuts import redirect, reverse, render, get_object_or_404
from rir_dashboard.forms.indicator import IndicatorForm
from rir_dashboard.views.dashboard.admin._base import AdminView
from rir_data.models import Indicator, Instance


class IndicatorCreateView(AdminView):
    template_name = 'dashboard/admin/indicator/new.html'
    indicator = None
    scenario_level = None

    @property
    def dashboard_title(self):
        return f'<span>Create New Indicator</span>'

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        try:
            context = {
                'form': IndicatorForm(
                    level=self.instance.geometry_levels_in_order,
                    instance=self.instance
                )
            }
            return context
        except Indicator.DoesNotExist:
            raise Http404('Indicator does not found')

    def post(self, request, **kwargs):
        self.instance = get_object_or_404(
            Instance, slug=kwargs.get('slug', '')
        )
        form = IndicatorForm(
            request.POST,
            level=self.instance.geometry_levels_in_order,
            instance=self.instance
        )
        if form.is_valid():
            form.save()
            return redirect(
                reverse(
                    'dashboard-view', args=[self.instance.slug]
                )
            )
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(
            request,
            self.template_name,
            context
        )

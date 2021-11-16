from django.shortcuts import redirect, reverse, render, get_object_or_404
from rir_dashboard.forms.indicator import IndicatorForm
from rir_dashboard.views.dashboard.admin._base import AdminView
from rir_data.models import Instance, ScenarioLevel, IndicatorScenarioRule


class IndicatorCreateView(AdminView):
    template_name = 'dashboard/admin/indicator/form.html'

    @property
    def dashboard_title(self):
        return f'<span>Create New Indicator</span>'

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        scenarios = []
        for scenario in ScenarioLevel.objects.order_by('level'):
            scenarios.append({
                'id': scenario.id,
                'name': scenario.name,
            })
        context = {
            'form': IndicatorForm(
                level=self.instance.geometry_levels_in_order,
                indicator_instance=self.instance
            ),
            'scenarios': scenarios
        }
        return context

    def post(self, request, **kwargs):
        self.instance = get_object_or_404(
            Instance, slug=kwargs.get('slug', '')
        )
        form = IndicatorForm(
            request.POST,
            level=self.instance.geometry_levels_in_order,
            indicator_instance=self.instance
        )
        if form.is_valid():
            indicator = form.save()
            for scenario in ScenarioLevel.objects.order_by('level'):
                rule = request.POST.get(f'scenario_{scenario.id}_rule', None)
                name = request.POST.get(f'scenario_{scenario.id}_name', None)
                if rule and name:
                    scenario_rule, created = IndicatorScenarioRule.objects.get_or_create(
                        indicator=indicator,
                        scenario_level=scenario
                    )
                    scenario_rule.name = name
                    scenario_rule.rule = rule
                    scenario_rule.save()
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

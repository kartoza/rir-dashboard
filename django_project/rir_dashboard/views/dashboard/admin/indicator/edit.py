from django.http import Http404
from django.shortcuts import redirect, reverse, render, get_object_or_404
from rir_dashboard.forms.indicator import IndicatorForm
from rir_dashboard.views.dashboard.admin._base import AdminView
from rir_data.models import Indicator, Instance, ScenarioLevel, IndicatorScenarioRule


class IndicatorEditView(AdminView):
    template_name = 'dashboard/admin/indicator/form.html'

    @property
    def dashboard_title(self):
        return f'<span>Edit Indicator</span>'

    @property
    def context_view(self) -> dict:
        """
        Return context for specific view by instance
        """
        try:
            indicator = self.instance.indicators.get(
                id=self.kwargs.get('pk', '')
            )
        except Indicator.DoesNotExist:
            raise Http404('Indicator does not exist')

        scenarios = []
        for scenario in ScenarioLevel.objects.order_by('level'):
            try:
                scenario_rule = IndicatorScenarioRule.objects.get(
                    scenario_level=scenario,
                    indicator=indicator
                )
            except IndicatorScenarioRule.DoesNotExist:
                scenario_rule = None
            scenarios.append({
                'id': scenario.id,
                'name': scenario.name,
                'rule_name': scenario_rule.name if scenario_rule else '',
                'rule_value': scenario_rule.rule if scenario_rule else '',
                'rule_color': scenario_rule.color if scenario_rule else '',
            })
        context = {
            'form': IndicatorForm(
                initial=IndicatorForm.model_to_initial(indicator),
                level=self.instance.geometry_levels_in_order,
                indicator_instance=self.instance,
                indicator_object=indicator,
            ),
            'scenarios': scenarios
        }
        return context

    def post(self, request, **kwargs):
        self.instance = get_object_or_404(
            Instance, slug=kwargs.get('slug', '')
        )
        try:
            indicator = self.instance.indicators.get(
                id=self.kwargs.get('pk', '')
            )
        except Indicator.DoesNotExist:
            raise Http404('Indicator does not exist')

        form = IndicatorForm(
            request.POST,
            instance=indicator,
            level=self.instance.geometry_levels_in_order,
            indicator_instance=self.instance
        )
        if form.is_valid():
            indicator = form.save()
            for scenario in ScenarioLevel.objects.order_by('level'):
                rule = request.POST.get(f'scenario_{scenario.id}_rule', None)
                name = request.POST.get(f'scenario_{scenario.id}_name', None)
                color = request.POST.get(f'scenario_{scenario.id}_color', None)
                if rule and name:
                    scenario_rule, created = IndicatorScenarioRule.objects.get_or_create(
                        indicator=indicator,
                        scenario_level=scenario
                    )
                    scenario_rule.name = name
                    scenario_rule.rule = rule
                    scenario_rule.color = color
                    scenario_rule.save()
            return redirect(
                reverse(
                    'indicator-management-view', args=[self.instance.slug]
                )
            )
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(
            request,
            self.template_name,
            context
        )

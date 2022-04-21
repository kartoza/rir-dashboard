from django.shortcuts import redirect, reverse, render, get_object_or_404
from rir_dashboard.forms.indicator import IndicatorForm
from rir_dashboard.views.dashboard.admin._base import AdminView
from rir_data.models import Instance, ScenarioLevel, IndicatorScenarioRule, Indicator


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
                'rule_name': scenario.name,
                'rule_color': scenario.background_color
            })

        from_id = self.request.GET.get('from')
        initial = None
        if from_id:
            try:
                indicator = self.instance.indicators.get(id=from_id)
                initial = IndicatorForm.model_to_initial(indicator)
                initial['name'] = None
                initial['description'] = None
                scenarios = indicator.scenarios_dict()
            except Indicator.DoesNotExist:
                pass

        context = {
            'form': IndicatorForm(
                indicator_instance=self.instance,
                initial=initial,
            ),
            'scenarios': scenarios,
            'is_create': True
        }
        return context

    def post(self, request, **kwargs):
        self.instance = get_object_or_404(
            Instance, slug=kwargs.get('slug', '')
        )
        form = IndicatorForm(
            request.POST,
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
        context['is_create'] = True
        return render(
            request,
            self.template_name,
            context
        )

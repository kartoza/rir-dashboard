from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from rir_data.models.indicator.indicator import Indicator
from rir_data.models.scenario import ScenarioLevel


class IndicatorScenarioRule(models.Model):
    """
    The rule of scenario
    """
    name = models.CharField(
        max_length=512
    )
    indicator = models.ForeignKey(
        Indicator,
        on_delete=models.CASCADE
    )
    scenario_level = models.ForeignKey(
        ScenarioLevel,
        on_delete=models.CASCADE
    )
    rule = models.CharField(
        max_length=256,
        help_text=_(
            'Use formula to create the rule and use x as the value.'
            'Example: x<100. '
            'It will replace x with the value and will check the condition.'
        )
    )
    color = models.CharField(
        max_length=16,
        null=True, blank=True,
        help_text=_(
            'Color that override the scenario level color'
        )
    )

    class Meta:
        unique_together = ('indicator', 'scenario_level')

    @property
    def rule_str(self):
        """ Return rules in string list
        """
        values = []
        if not self.rule:
            return ''
        rules = self.rule.lower().replace(' ', '').split('and')
        for rule in rules:
            current_symbol = None
            for symbol in ['<=', '>=', '==', '<', '>']:
                if symbol in rule:
                    current_symbol = symbol
                    break

            temp = rule.split(current_symbol)
            unit = ''
            if self.indicator.unit:
                unit = f'{self.indicator.unit}'

            str_symbol = '=' if current_symbol == '==' else symbol
            if temp[0] == 'x':
                values.append(f'{str_symbol}{temp[1]} {unit}')
            else:
                values.append(f'{temp[0]} {unit} {str_symbol}')

        return " & ".join(values)

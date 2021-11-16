from django import forms
from django.forms.models import model_to_dict
from rir_data.models.instance import Instance
from rir_data.models.indicator import (
    Indicator, IndicatorFrequency, IndicatorGroup, frequency_help_text,
)


class IndicatorForm(forms.ModelForm):
    """
    Indicator form
    """
    label_suffix = ""
    instance = forms.ModelChoiceField(
        Instance.objects.all()
    )
    frequency = forms.IntegerField(
        help_text=frequency_help_text
    )
    group = forms.CharField()

    def __init__(self, *args, **kwargs):
        level = None
        try:
            level = kwargs.pop("level")
        except KeyError:
            pass
        instance = kwargs.pop("indicator_instance")
        super().__init__(*args, **kwargs)
        if level:
            self.fields['geometry_reporting_level'].choices = [(u.id, u.name) for u in level]
        self.fields['instance'].initial = instance

    class Meta:
        model = Indicator
        exclude = ('unit', 'order', 'geometry_reporting_units')

    def clean_frequency(self):
        frequency = self.cleaned_data['frequency']
        indicator_frequency, created = IndicatorFrequency.objects.get_or_create(
            name=f'{frequency} days',
            frequency=frequency
        )
        return indicator_frequency

    def clean_group(self):
        group = self.cleaned_data['group']
        instance = Instance.objects.get(id=self.data['instance'])
        indicator_group, created = IndicatorGroup.objects.get_or_create(
            name=group,
            instance=instance
        )
        return indicator_group

    @staticmethod
    def model_to_initial(indicator: Indicator):
        from rir_data.models.indicator import IndicatorGroup
        from rir_data.models.indicator import IndicatorFrequency
        initial = model_to_dict(indicator)
        try:
            initial['group'] = IndicatorGroup.objects.get(id=initial['group']).name
        except IndicatorGroup.DoesNotExist:
            initial['group'] = None
        try:
            initial['frequency'] = IndicatorFrequency.objects.get(id=initial['frequency']).frequency
        except IndicatorGroup.DoesNotExist:
            initial['frequency'] = None
        return initial

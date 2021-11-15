from django import forms
from rir_data.models.instance import Instance
from rir_data.models.indicator import (
    Indicator, IndicatorFrequency, IndicatorGroup, frequency_help_text,
)


class IndicatorForm(forms.ModelForm):
    """
    Form to upload CSV file.
    """
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
        instance = kwargs.pop("instance")
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        if level:
            self.fields['geometry_reporting_level'].choices = [(u.id, u.name) for u in level]
        self.fields['instance'].initial = instance

    class Meta:
        model = Indicator
        exclude = ('unit',)

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

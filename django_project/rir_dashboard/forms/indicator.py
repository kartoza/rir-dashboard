import json
from django import forms
from django.forms.models import model_to_dict
from django.shortcuts import reverse
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
    api_exposed = forms.BooleanField(
        label='Expose API',
        required=False
    )

    def __init__(self, *args, **kwargs):
        level = None
        try:
            level = kwargs.pop("level")
        except KeyError:
            pass
        instance = kwargs.pop("indicator_instance")

        try:
            indicator_object = kwargs.pop("indicator_object")
        except KeyError:
            indicator_object = None

        super().__init__(*args, **kwargs)
        if level:
            self.fields['geometry_reporting_level'].choices = [(u.id, u.name) for u in level]
        self.fields['instance'].initial = instance

        self.fields['api_exposed'].help_text = 'Indicate that API is exposed outside. This API is used for get the data and also POST new data.'
        if indicator_object:
            api_url = reverse(
                'indicator-values-api', args=[instance.slug, indicator_object.id]
            )
            example = {
                "geometry_code": "SO",
                "extra_data": {
                    "Data 1": "1",
                    "Data 2": "2",
                },
                "date": "2022-01-01",
                "value": 1
            }
            view_geometry_url = reverse(
                'geography-management-view', args=[instance.slug]
            ) + '#' + indicator_object.geometry_reporting_level.name
            self.fields['api_exposed'].help_text = (
                f'<br>Can access the API with url : <a href="{api_url}">{api_url}</a>'
                f'<br>Use this token to access it : <b>{str(indicator_object.api_token)}</b>'
                f'<br>Provide this example data below to POST new Data.'
                f'<pre style="color: gray; font-size: 12px;">{json.dumps(example, indent=4, sort_keys=True)}</pre>'
                f'<span class="helptext">To check geometry code, go to <a href="{view_geometry_url}">{view_geometry_url}</a>, hover a geometry, and get the "code" as geometry code.</span>'
            )
        else:
            self.fields['api_exposed'].help_text += f'<br>The url of API will be created after the indicator created..'

    class Meta:
        model = Indicator
        exclude = ('unit', 'order', 'geometry_reporting_units', 'instance')

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

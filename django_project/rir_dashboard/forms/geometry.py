import json
from django import forms
from django.core.exceptions import ValidationError
from rir_data.models.geometry import GeometryLevelName

ADD_JUST_NEW = 'Just add new geometry'
REPLACE_AND_ADD = 'Replace and add everything'
CHOICES = (
    (ADD_JUST_NEW, ADD_JUST_NEW),
    # (REPLACE_AND_ADD, REPLACE_AND_ADD)
)


class GeometryForm(forms.Form):
    """
    Form to upload CSV file.
    """
    label_suffix = ""

    level = forms.ModelChoiceField(
        GeometryLevelName.objects.all()
    )
    code_column = forms.CharField(
        help_text='Column name on the geojson that is code.',
    )
    name_column = forms.CharField(
        help_text='Column name on the geojson that is name.',
    )
    parent_code_column = forms.CharField(
        help_text='[Optional] Column code on the geojson that is code of parent.',
        required=False
    )
    replace_method = forms.ChoiceField(
        choices=CHOICES
    )
    geojson = forms.FileField()

    def __init__(self, *args, **kwargs):
        level = None
        try:
            level = kwargs.pop("level")
        except KeyError:
            pass
        super().__init__(*args, **kwargs)
        if level:
            self.fields['level'].choices = [(u.id, u.name) for u in level]

    def clean_geojson(self):
        geojson = self.cleaned_data['geojson']
        name_column = self.cleaned_data['name_column']
        code_column = self.cleaned_data['code_column']
        parent_code_column = self.cleaned_data['parent_code_column']
        objects = json.load(geojson)

        features = []
        for feature in objects['features']:
            properties = feature['properties']
            try:
                feature['properties'] = {
                    'name': properties[name_column],
                    'identifier': f'{properties[code_column]}',
                    'parent_identifier': f'{properties.get(parent_code_column)}',
                }
                features.append(feature)
            except KeyError as e:
                raise ValidationError(f'No column named {e}')

        return {
            "type": "FeatureCollection",
            "features": features
        }

from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from rir_data.models.instance import Instance


class InstanceForm(forms.ModelForm):
    """
    Form to upload CSV file.
    """
    label_suffix = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Instance
        exclude = ('slug', 'white_icon')

    def clean_name(self):
        name = self.cleaned_data['name']
        if self.instance.name_is_exist(name):
            raise ValidationError('This name already exist')
        return name

    @staticmethod
    def model_to_initial(instance: Instance):
        return model_to_dict(instance)

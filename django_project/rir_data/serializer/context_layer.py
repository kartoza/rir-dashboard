import urllib.parse
from rest_framework import serializers
from rir_data.models.context_layer import ContextLayer, ContextLayerParameter


class ContextLayerSerializer(serializers.ModelSerializer):
    parameters = serializers.SerializerMethodField()
    group_name = serializers.SerializerMethodField()

    def get_parameters(self, obj: ContextLayer):
        parameters = {}
        for parameter in obj.contextlayerparameter_set.all():
            value = parameter.value
            try:
                if value is None:
                    value = ''
                value = int(parameter.value)
            except (ValueError, TypeError):
                value = urllib.parse.quote(value)
            parameters[parameter.name] = value
        return parameters

    def get_group_name(self, obj: ContextLayer):
        return obj.group.name if obj.group else ''

    class Meta:
        model = ContextLayer
        fields = '__all__'


class ContextLayerParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContextLayerParameter
        fields = '__all__'

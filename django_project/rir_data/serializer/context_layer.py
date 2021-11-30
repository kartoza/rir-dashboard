from rest_framework import serializers
from rir_data.models.context_layer import ContextLayer, ContextLayerParameter


class ContextLayerSerializer(serializers.ModelSerializer):
    parameters = serializers.SerializerMethodField()

    def get_parameters(self, obj: ContextLayer):
        parameters = {}
        for parameter in obj.contextlayerparameter_set.all():
            value = parameter.value
            try:
                if value is None:
                    value = ''
                value = int(parameter.value)
            except (ValueError, TypeError):
                pass
            parameters[parameter.name] = value
        return parameters

    class Meta:
        model = ContextLayer
        fields = '__all__'


class ContextLayerParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContextLayerParameter
        fields = '__all__'

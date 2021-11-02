from rest_framework import serializers
from rir_data.models.instance import Instance


class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance
        fields = '__all__'

from rest_framework import serializers
from scenario.models.scenario import ScenarioLevel


class ScenarioLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScenarioLevel
        fields = '__all__'

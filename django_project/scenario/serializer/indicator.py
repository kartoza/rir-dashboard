from rest_framework import serializers
from scenario.models.indicator import Indicator


class IndicatorSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()
    scenario_level = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    def get_group(self, obj: Indicator):
        return obj.group.name

    def get_scenario_level(self, obj: Indicator):
        return obj.scenario_level.level

    def get_value(self, obj: Indicator):
        return obj.value

    class Meta:
        model = Indicator
        fields = ('id', 'group', 'scenario_level', 'value', 'name', 'description')

    def to_representation(self, instance: Indicator):
        data = super(IndicatorSerializer, self).to_representation(instance)
        for indicator_rule in instance.indicatorscenariorule_set.all():
            data[f'scenario_{indicator_rule.scenario_level.level}'] = indicator_rule.name
        return data

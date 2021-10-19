from rest_framework import serializers
from rir_data.models.indicator import Indicator


class IndicatorSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()

    def get_group(self, obj: Indicator):
        return obj.group.name

    class Meta:
        model = Indicator
        fields = ('id', 'group', 'name', 'description', 'show_in_traffic_light', 'unit')

    def to_representation(self, instance: Indicator):
        data = super(IndicatorSerializer, self).to_representation(instance)
        for indicator_rule in instance.indicatorscenariorule_set.all():
            data[f'scenario_{indicator_rule.scenario_level.level}'] = indicator_rule.name
        return data

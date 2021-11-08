from rest_framework import serializers
from rir_data.models.indicator import Indicator, IndicatorValue


class IndicatorSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()

    def get_group(self, obj: Indicator):
        return obj.group.name

    class Meta:
        model = Indicator
        fields = ('id', 'group', 'name', 'show_in_traffic_light')

    def to_representation(self, instance: Indicator):
        data = super(IndicatorSerializer, self).to_representation(instance)
        for indicator_rule in instance.indicatorscenariorule_set.all():
            data[f'scenario_{indicator_rule.scenario_level.level}'] = indicator_rule.name
        return data


class IndicatorValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorValue
        fields = '__all__'

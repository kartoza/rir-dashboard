from rest_framework import serializers
from rir_data.models.program import Program


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'

    def to_representation(self, instance: Program):
        data = super(ProgramSerializer, self).to_representation(instance)
        for intervention in instance.programintervention_set.all():
            data[f'scenario_{intervention.scenario_level.level}'] = intervention.intervention_url
        return data

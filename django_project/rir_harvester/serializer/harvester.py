from rest_framework import serializers
from rir_harvester.models.harvester_log import HarvesterLog


class HarvesterLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HarvesterLog
        fields = '__all__'

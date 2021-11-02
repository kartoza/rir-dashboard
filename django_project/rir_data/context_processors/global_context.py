from rir_data.models.instance import Instance
from rir_data.serializer.instance import InstanceSerializer


def global_context(request):
    return {
        'instances': InstanceSerializer(Instance.objects.order_by('name'), many=True).data
    }

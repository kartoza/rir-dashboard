from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rir_data.models.geometry import Geometry


class GeometrySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Geometry
        geo_field = 'geometry'
        fields = '__all__'

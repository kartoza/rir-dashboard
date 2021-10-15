import json
import os
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon
from core.models import Geometry, GeometryLevel
from core.settings.utils import DJANGO_ROOT


def run():
    """ Run importer geometries of somalia """
    folder = os.path.join(DJANGO_ROOT, 'core', 'fixtures', 'somalia')

    try:
        # country level
        country_level = GeometryLevel.objects.get(name__iexact='country')
        geojson = json.load(
            open(os.path.join(folder, 'som_adm_0.geojson'))
        )
        for feature in geojson['features']:
            properties = feature['properties']
            Geometry.objects.get_or_create(
                identifier=properties['admin0Pcod'],
                geometry_level=country_level,
                defaults={
                    'name': properties['admin0Name'],
                    'geometry': GEOSGeometry(
                        json.dumps(feature['geometry'])
                    )
                }
            )

        # region level
        region_level = GeometryLevel.objects.get(name__iexact='region')
        geojson = json.load(
            open(os.path.join(folder, 'som_adm_1.geojson'))
        )
        for feature in geojson['features']:
            properties = feature['properties']

            # get the country
            country = Geometry.objects.get(
                identifier=properties['admin0Pcod'],
                geometry_level=country_level
            )
            # save the geometry
            Geometry.objects.get_or_create(
                identifier=properties['admin1Pcod'],
                geometry_level=region_level,
                child_of=country,
                defaults={
                    'name': properties['admin1Name'],
                    'alias': properties['admin1AltN'],
                    'geometry': GEOSGeometry(
                        json.dumps(feature['geometry'])
                    )
                }
            )

        # district level
        district_level = GeometryLevel.objects.get(name__iexact='district')
        geojson = json.load(
            open(os.path.join(folder, 'som_adm_2.geojson'))
        )
        for feature in geojson['features']:
            properties = feature['properties']
            # get the country
            region = Geometry.objects.get(
                identifier=properties['admin1Pcod'],
                geometry_level=region_level
            )
            # save the geometry
            geometry = GEOSGeometry(
                json.dumps(feature['geometry'])
            )
            if isinstance(geometry, Polygon):
                geometry = MultiPolygon(geometry)
            Geometry.objects.get_or_create(
                identifier=properties['admin2Pcod'],
                geometry_level=district_level,
                child_of=region,
                defaults={
                    'name': properties['admin2Name'],
                    'alias': properties['admin2AltN'],
                    'geometry': geometry
                }
            )
    except (Geometry.DoesNotExist, GeometryLevel.DoesNotExist):
        pass

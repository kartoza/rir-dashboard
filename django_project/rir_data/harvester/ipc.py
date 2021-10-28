from datetime import datetime
from rir_data.harvester.base import (
    BaseHarvester, HarvestingError
)
from rir_data.models import Geometry, GeometryLevelName
from rir_data.models.indicator import IndicatorExtraValue


class PopulationTrackingTool(BaseHarvester):
    """
    Harvester for population tracking tool
    """
    url = 'http://mapipcissprd.us-east-1.elasticbeanstalk.com/api/public/population-tracking-tool/data/2016,2021/?page=1&limit=100&condition=A&country={}'

    @staticmethod
    def additional_attributes() -> dict:
        """
        """
        return {
            'country_code': None
        }

    def _process(self):
        """ Run the harvester """
        try:
            country_code = self.attributes['country_code']
        except KeyError as e:
            raise HarvestingError(f'{e} is not provided.')

        country_level = GeometryLevelName.objects.get(name__iexact='country')
        region_level = GeometryLevelName.objects.get(name__iexact='region')
        district_level = GeometryLevelName.objects.get(name__iexact='district')

        country = Geometry.objects.get(
            geometry_level=country_level,
            identifier__iexact=country_code
        )

        response = self._request_api(self.url.format(country_code))
        for row in response.json():
            region_name = row['group_name']
            district_name = row['area']
            try:
                # formatting name
                region = Geometry.objects.get_by(
                    region_name, region_level, country
                )
                district = Geometry.objects.get_by(
                    district_name, district_level, region
                )
                date_data = row['fanalysis_date']
                date_data = datetime.strptime(date_data, "%Y%m%d").date()
                value = row['overall_phase']
                indicator_value = self.save_indicator_data(
                    value, date_data, district
                )
                # save additional data
                for key, name in {
                    'phase1_C_population': 'Phase 1 population',
                    'phase2_C_population': 'Phase 2 population',
                    'phase3_C_population': 'Phase 3 population',
                    'phase4_C_population': 'Phase 4 population',
                    'phase5_C_population': 'Phase 5 population',
                }.items():
                    try:
                        IndicatorExtraValue.objects.get_or_create(
                            indicator_value=indicator_value,
                            name=name,
                            defaults={
                                'value': row[key]
                            }
                        )
                    except KeyError:
                        pass

            except Geometry.DoesNotExist:
                print(f'Not found : {region_name} - {district_name}')

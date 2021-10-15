from scenario.harvester.base import (
    BaseHarvester, HarvestingError
)


class BasicAPI(BaseHarvester):
    """
    Harvester just get the data from api and get the data from response
    """

    @staticmethod
    def additional_attributes() -> dict:
        """
        api_url: URL of api
        data_keys: Key of data in comma separator
                   example: features.0.attributes.value
                            it will check data['features'][0]['attributes']['value']
        """
        return {
            'api_url': None,
            'data_keys': None,
        }

    def _process(self):
        """ Run the harvester """
        try:
            api_url = self.attributes['api_url']
            data_keys = self.attributes['data_keys']
        except KeyError as e:
            raise HarvestingError(f'{e} is not provided.')

        # fetch stations first
        response = self._request_api(api_url)
        data = response.json()
        keys = data_keys.split('.')

        try:
            value = data
            for key in keys:
                # if instance is list
                # make key as integer
                if isinstance(value, list):
                    key = int(key)

                value = value[key]
        except ValueError as e:
            raise HarvestingError(f'{e}')
        except (KeyError, IndexError) as e:
            raise HarvestingError(f'{e} is not found on data. Data:{data}')
        else:
            self.save_indicator_data(value)

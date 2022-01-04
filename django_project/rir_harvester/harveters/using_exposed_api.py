from rir_harvester.harveters._base import BaseHarvester


class UsingExposedAPI(BaseHarvester):
    """
    Harvester to indicate the indicator is just receiving data using exposed API from external client
    """
    description = "Harvester to indicate the indicator is just receiving data using exposed API from external client"

    @staticmethod
    def additional_attributes() -> dict:
        return {}

    def _process(self):
        """ Run the harvester """
        return

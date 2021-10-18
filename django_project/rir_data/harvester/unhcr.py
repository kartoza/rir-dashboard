import csv
import requests
from rir_data.harvester.base import (
    BaseHarvester, HarvestingError
)


class DatavizSomalia(BaseHarvester):
    """
    Harvester for unhcr
    """
    csv_url = 'https://unhcr.github.io/dataviz-somalia-prmn/data/PRMNDataset.csv'

    def _process(self):
        """ Run the harvester """

        with requests.Session() as s:
            download = s.get(self.csv_url)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            # TODO:
            #  We have arrival and departure district
            #  how to distinct the data

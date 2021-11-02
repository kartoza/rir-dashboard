from django.contrib.gis.db import models
from core.models import AbstractTerm
from rir_data.models.instance import Instance
from rir_data.models.scenario import ScenarioLevel


class Program(AbstractTerm):
    """
    Program
    """
    instance = models.ForeignKey(
        Instance,
        on_delete=models.CASCADE
    )


class ProgramIntervention(models.Model):
    """
    Intervention of program
    """
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE
    )
    scenario_level = models.ForeignKey(
        ScenarioLevel, on_delete=models.CASCADE
    )
    intervention_url = models.TextField()

    class Meta:
        unique_together = ('program', 'scenario_level')

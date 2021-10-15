from django.contrib.gis.db import models
from core.models import AbstractTerm
from .scenario import ScenarioLevel


class Program(AbstractTerm):
    """
    Program
    """
    pass


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

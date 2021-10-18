from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from rir_data.models.harvester import Harvester


class LogStatus(object):
    RUNNING = 'Running'
    ERROR = 'Error'
    DONE = 'Done'


class HarvesterLog(models.Model):
    """ History of harvester """
    harvester = models.ForeignKey(
        Harvester, on_delete=models.CASCADE
    )
    start_time = models.DateTimeField(
        auto_now_add=True,
        help_text=_(
            "This is when the harvester is started.")
    )
    end_time = models.DateTimeField(
        blank=True, null=True
    )
    status = models.CharField(
        max_length=100,
        choices=(
            (LogStatus.RUNNING, _(LogStatus.RUNNING)),
            (LogStatus.ERROR, _(LogStatus.ERROR)),
            (LogStatus.DONE, _(LogStatus.DONE)),
        ),
        default=LogStatus.RUNNING
    )
    note = models.TextField(
        blank=True, null=True
    )

    class Meta:
        ordering = ('-start_time',)

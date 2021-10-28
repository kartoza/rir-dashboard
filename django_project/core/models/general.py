from django.contrib.gis.db import models
from django.template.defaultfilters import slugify


class AbstractTerm(models.Model):
    """ Abstract model for Term """

    slug = models.SlugField(
        max_length=512, unique=True
    )
    name = models.CharField(
        max_length=512
    )
    description = models.TextField(
        null=True, blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True

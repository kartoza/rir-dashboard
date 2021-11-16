from django.contrib.gis.db import models
from django.template.defaultfilters import slugify


class AbstractTerm(models.Model):
    """ Abstract model for Term """
    name = models.CharField(
        max_length=512
    )
    description = models.TextField(
        null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class SlugTerm(AbstractTerm):
    """ Abstract model for Term """

    slug = models.SlugField(
        max_length=512, unique=True
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True

    def name_is_exist(self, name: str) -> bool:
        """
        Check of name is exist
        """
        return self._meta.model.objects.exclude(pk=self.pk).filter(
            slug=slugify(name)
        ).first() is not None


class IconTerm(models.Model):
    """ Abstract model contains icon """
    icon = models.FileField(
        upload_to='icons',
        null=True,
        blank=True
    )
    white_icon = models.FileField(
        upload_to='icons',
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

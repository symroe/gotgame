from django.db import models
from model_utils.models import TimeStampedModel


class ConsoleNetwork(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Console(TimeStampedModel):
    name = models.CharField(max_length=255)
    network = models.ForeignKey(ConsoleNetwork)

    def __unicode__(self):
        return self.name


class Title(TimeStampedModel):
    name = models.CharField(blank=True, max_length=255)
    console = models.ForeignKey(Console)
    # From easports.com
    platformTag = models.CharField(blank=True, max_length=255)

    def __unicode__(self):
        return self.platformTag

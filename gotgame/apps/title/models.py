from django.db import models
from model_utils.models import TimeStampedModel


class Console(TimeStampedModel):
    # TODO move this to it's own app?
    name = models.CharField(blank=True, max_length=255)
    
    def __unicode__(self):
        return self.name

class Title(TimeStampedModel):
    name = models.CharField(blank=True, max_length=255)
    console = models.ForeignKey(Console)
    # From easports.com
    platformTag = models.CharField(blank=True, max_length=255) 
    
    def __unicode__(self):
        return self.platformTag
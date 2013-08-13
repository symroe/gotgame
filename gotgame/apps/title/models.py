from django.db import models

class Console(models.Model):
    # TODO move this to it's own app?
    name = models.CharField(blank=True, max_length=255)

class Title(models.Model):
    name = models.CharField(blank=True, max_length=255)
    console = models.ForeignKey(Console)
    # From easports.com
    platformTag = models.CharField(blank=True, max_length=255) 
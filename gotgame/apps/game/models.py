import datetime

from django.db import models

from model_utils.models import TimeStampedModel

from title.models import Title


class Game(TimeStampedModel):
    started = models.DateTimeField(blank=True, default=datetime.datetime.now)
    ended = models.DateTimeField(blank=True, null=True)
    title = models.ForeignKey(Title)
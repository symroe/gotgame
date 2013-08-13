from django.db import models
from model_utils.models import TimeStampedModel

from titles.models import Console, Title

import constants

class Player(TimeStampedModel):
    credits = models.IntegerField(blank=False, null=False, default=0)
    
    def add_credit(self, amount):
        self.credits = self.credits + amount
    
    def minus_credit(self, amount):
        self.credits = self.credits - amount


class PlayerResult(TimeStampedModel):
    player = models.ForeignKey(Player)
    result = models.CharField(blank=True, max_length=100,
        choices=constants.GAME_RESULTS)


class PlayerConsole(models.Model):
    console = models.ForeignKey(Console)
    player = models.ForeignKey(Player)
    gamer_tag = models.CharField(blank=True, max_length=100)

class PlayerTitle(models.Model):
    # TODO many to many?
    title = models.ForeignKey(Title)
    player = models.ForeignKey(Player)


class Banked(TimeStampedModel):
    player = models.ForeignKey(Player)
    credits = models.IntegerField(default=0)
    
    def __unicode__(self):
        return u'Banked %s credits for %s' % (self.credits, self.profile)

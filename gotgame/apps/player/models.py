from django.db import models
from model_utils.models import TimeStampedModel

from title.models import Console, Title

class Player(TimeStampedModel):
    """
    This is the main player model.  A player is exactly the same as a user.
    
    A player can own different titles and consoles.
    
    A player buys credits and has them available.  They can't start a new streak
    if credits are 0.
    """
    credits = models.IntegerField(blank=False, null=False, default=0)
    consoles = models.ManyToManyField(Console, through='PlayerConsole')
    titles = models.ManyToManyField(Title)
    
    def add_credit(self, amount):
        self.credits = self.credits + amount
    
    def minus_credit(self, amount):
        self.credits = self.credits - amount


class PlayerConsole(models.Model):
    """
    A through model from player to console.  Used to store gamer_tag against
    console.
    """
    console = models.ForeignKey(Console)
    player = models.ForeignKey(Player)
    gamer_tag = models.CharField(blank=True, max_length=100)


class Cashout(TimeStampedModel):
    """
    A cashout is a record of the amount of money owed by GotGame to the player.
    
    Cashouts are one way: once a user puts credits in the cashout they are not 
    able to withdraw them.
    """
    player = models.ForeignKey(Player)
    amount = models.IntegerField(default=0)
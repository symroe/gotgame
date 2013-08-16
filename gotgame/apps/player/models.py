from django.db import models
from model_utils.models import TimeStampedModel
from timezone_field import TimeZoneField
from jsonfield import JSONField

from core.strings import generate_random_unique_field

from title.models import Console, Title

class Player(TimeStampedModel):
    """
    This is the main player model.  A player is exactly the same as a user.

    A player can own different titles and consoles.

    A player buys credits and has them available.  They can't start a new streak
    if credits are 0.
    """

    id = models.CharField(max_length=40, primary_key=True, editable=False)

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    timezone = TimeZoneField(blank=True, null=True)

    fb_id = models.CharField(max_length=150, unique=True)
    fb_json = JSONField()
    fb_token = models.CharField(max_length=500, unique=True)
    active = models.BooleanField(default=True)

    credits = models.IntegerField(blank=False, null=False, default=0)
    consoles = models.ManyToManyField(Console, through='PlayerConsole')
    titles = models.ManyToManyField(Title)

    def add_credit(self, amount):
        self.credits = self.credits + amount

    def minus_credit(self, amount):
        self.credits = self.credits - amount


    def save(self, *args, **kwargs):
        """
            Creates a hashed id.
        """

        # creating id if not set
        if not self.id:
            self.id = generate_random_unique_field(self.__class__)
        super(Player, self).save(*args, **kwargs)


class PlayerConsole(TimeStampedModel):
    """
    A through model from player to console.  Used to store gamer_tag against
    console.
    """
    console = models.ForeignKey(Console)
    player = models.ForeignKey(Player)
    gamer_tag = models.CharField(blank=False, max_length=100)


class CashoutRequest(TimeStampedModel):
    """
    A cashout is a record of the amount of money owed by GotGame to the player.

    Cashouts are one way: once a user puts credits in the cashout they are not
    able to withdraw them.
    """
    player = models.ForeignKey(Player)
    amount = models.IntegerField(default=0)
    status = models.CharField(blank=True, max_length=100)
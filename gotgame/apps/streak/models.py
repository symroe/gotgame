import datetime

from django.db import models

from model_utils.models import TimeStampedModel

from player.models import Player
from title.models import Title, Console

import constants

class Streak(models.Model):
    """
    A streak is a run of games.  Streaks are started with player credits and are
    ended when a player looses a game.
    
    Each time a player wins, the current_level is doubled.
    """
    player = models.ForeignKey(Player)
    current_level = models.IntegerField(blank=True, null=True, choices=constants.valid_levels())


class StreakGame(models.Model):
    """
    Stores the level, title and result of a game a player played.
    """
    started = models.DateTimeField(blank=True, default=datetime.datetime.now)
    ended = models.DateTimeField(blank=True, null=True)
    streak = models.ForeignKey(Streak)
    title = models.ForeignKey(Title)
    result = models.ForeignKey('StreakGameResult')
    game_level = models.IntegerField(blank=True, null=True, choices=constants.valid_levels())



class StreakGameResult(TimeStampedModel):
    """
    Stores all the results for games a player has played.  This
    """
    player = models.ForeignKey(Player)
    own_score = models.CharField(blank=True, max_length=10)
    opponent_score = models.CharField(blank=True, max_length=10)
    result = models.CharField(blank=True, max_length=100,
        choices=constants.GAME_RESULTS)
    title = models.ForeignKey(Title)
    console = models.ForeignKey(Console)



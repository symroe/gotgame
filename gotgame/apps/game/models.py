from django.db import models

from model_utils.models import TimeStampedModel


class Profile(TimeStampedModel):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    credits = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s - %s' % (self.username, self.email)


class Banked(TimeStampedModel):
    profile = models.ForeignKey(Profile)
    credits = models.IntegerField(default=0)

    def __unicode__(self):
        return u'Banked %s credits for %s' % (self.credits, self.profile)

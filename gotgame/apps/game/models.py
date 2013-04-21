from django.db import models


class Profile(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    credits = models.IntegerField(default=0)


class Banked(models.Model):
    profile = models.ForeignKey(Profile)
    credits = models.IntegerField(default=0)

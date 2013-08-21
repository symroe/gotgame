from django.contrib import admin

from streak.models import Streak
from .models import Player, PlayerConsoleNetwork

class PlayerConsoleNetworkInline(admin.StackedInline):
    model = PlayerConsoleNetwork
    extra = 0

class PlayerStreakInline(admin.StackedInline):
    model = Streak
    extra = 0


class PlayerAdmin(admin.ModelAdmin):
    inlines = [PlayerStreakInline, PlayerConsoleNetworkInline]


admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerConsoleNetwork)



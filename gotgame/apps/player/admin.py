from django.contrib import admin

from streak.models import Streak
from .models import Player, PlayerConsole

class PlayerConsoleInline(admin.StackedInline):
    model = PlayerConsole
    extra = 0

class PlayerStreakInline(admin.StackedInline):
    model = Streak
    extra = 0


class PlayerAdmin(admin.ModelAdmin):
    inlines = [PlayerStreakInline, PlayerConsoleInline]
    

admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerConsole)



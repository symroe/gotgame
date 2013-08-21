from django.contrib import admin

from .models import Title, Console, ConsoleNetwork


admin.site.register(Title)
admin.site.register(Console)
admin.site.register(ConsoleNetwork)

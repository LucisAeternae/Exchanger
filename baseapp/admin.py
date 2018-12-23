from django.contrib import admin
from baseapp.models import Game, Category, Profile, Offer

class GameAdmin(admin.ModelAdmin):
    pass


admin.site.register(Game)
admin.site.register(Category)
admin.site.register(Offer)

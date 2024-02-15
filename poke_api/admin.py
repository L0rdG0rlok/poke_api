from django.contrib import admin
from poke_api import models


admin.site.register(models.UserProfile)
admin.site.register(models.Pokemon)

import imp
from django.contrib import admin
from . import models

admin.site.register(models.Temple)
admin.site.register(models.Service)
admin.site.register(models.TempleService)
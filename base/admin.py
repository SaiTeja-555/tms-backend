from django.contrib import admin
from . import models

admin.site.register(models.Temple)
admin.site.register(models.Service)
admin.site.register(models.TempleService)
admin.site.register(models.ServiceBooking)
admin.site.register(models.TemplePic)
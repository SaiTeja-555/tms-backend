from django.db import models
from django.contrib.auth.models import User

# Temple
class Temple(models.Model):
    name = models.CharField(max_length= 100)
    admin = models.ForeignKey(User, on_delete= models.SET_NULL, null= True)
    registered_on = models.DateField(auto_now_add = True)
    dist = models.CharField(max_length= 50, null = True)
    locality = models.CharField(max_length= 100, null = True)
    pincode = models.CharField(max_length=10, null = True)

# Service
class Service(models.Model):
    name = models.CharField(max_length= 100)
    created_on = models.DateField(auto_now_add = True)

# Temple-Service
class TempleService(models.Model):
    temple_id = models.ForeignKey(Temple, on_delete= models.SET_NULL, null= True)
    service_id = models.ForeignKey(Service, on_delete= models.SET_NULL, null= True)
    cost = models.IntegerField(null= True)
    no_of_slots = models.PositiveIntegerField
    status = models.CharField(max_length= 20)
    created_on = models.DateField(auto_now_add = True)

class ServiceBooking(models.Model):
    templeservice_id = models.ForeignKey(TempleService, on_delete= models.SET_NULL, null= True)
    slot_index = models.IntegerField(null = True)
    service_date = models.DateField(null = True)
    booked_on = models.DateField(auto_now_add = True)
    status = models.CharField(max_length= 20)   
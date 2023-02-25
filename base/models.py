from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager,PermissionsMixin

from authentication.models import User
# from traitlets import default


def temples_upload_to(instance, filename):
    return 'uploads/temples/{filename}'.format(filename=filename)

def services_upload_to(instance, filename):
    return 'uploads/services/{filename}'.format(filename=filename)

def gallery_upload_to(instance, filename):
    return 'uploads/gallery/{filename}'.format(filename=filename)


# class CustomUserManager(BaseUserManager):
#     def create_user(self, username, email, password=None):

#         user = self.model(
#             username = username,
#             email = self.normalize_email(email),
#         )
#         user.set_password(password)
#         user.save(using = self._db)

#         return user
    
#     def create_superuser(self, username, email, password):
#         user = self.create_user(
#             username,
#             email,
#             password = password
#         )

#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using = self._db)
        
#         return user

# class CustomUser(AbstractUser):
#     id = models.AutoField(primary_key=True, editable=False)
#     phone = models.CharField(max_length=14, null=True)
#     area = models.CharField(max_length=50,null=True)
#     USERNAME_FIELD: id

    # objects = CustomUserManager()

# class Profile(models.Model):
#     ROLE_CHOICES = [
#         (1,"Super Admin"),
#         (2,"Admin"),
#         (3,"Visitor")
#     ]
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
#     phone = models.CharField(max_length=14, null=True)
#     role = models.PositiveSmallIntegerField(choices = ROLE_CHOICES)
#     area = models.CharField(max_length=50)



# Temple
class Temple(models.Model):
    name = models.CharField(max_length= 100)
    nameTel = models.CharField(max_length=100, null = True, blank=True)
    img = models.ImageField(upload_to=temples_upload_to,blank= True, null=True)
    admin = models.ForeignKey(User, on_delete= models.SET_NULL, null= True)
    registered_on = models.DateField(auto_now_add = True)
    dist = models.CharField(max_length= 50)
    pincode = models.CharField(max_length=10, null = True, blank=True)
    main_deity = models.CharField(max_length=50,default="saraswathi")
    sub_deities = models.CharField(null=True, blank=True, max_length=300); 
    fests = models.CharField(null=True, blank=True, max_length=300);
    location = models.CharField(max_length=50, null=True, blank=True)
    place = models.CharField(max_length=25)
    state = models.CharField(max_length=20)
    arch_type = models.CharField(max_length=20, null=True, blank=True)
    elevation = models.CharField(max_length=15, null=True, blank=True)
    intro = models.TextField(null=True, blank=True);
    history = models.TextField(null=True, blank=True);
    cur_status = models.TextField(null=True, blank=True);

# Service
class Service(models.Model):
    name = models.CharField(max_length= 100)
    created_on = models.DateField(auto_now_add = True)
    img = models.ImageField(upload_to=services_upload_to, null=True, blank=True)

# Temple-Service
class TempleService(models.Model):
    temple_id = models.ForeignKey(Temple, on_delete= models.CASCADE)
    service_id = models.ForeignKey(Service, on_delete= models.CASCADE)
    cost = models.IntegerField()
    duration = models.PositiveIntegerField()
    slots = models.JSONField(null=True)
    slot_capacity = models.PositiveIntegerField()
    status = models.CharField(max_length= 20)
    created_on = models.DateField(auto_now_add = True)


class ServiceBooking(models.Model):
    templeservice_id = models.ForeignKey(TempleService, on_delete= models.SET_NULL, null= True)
    slot_index = models.IntegerField(null = True)
    service_date = models.DateField(null = True)
    booked_on = models.DateField(auto_now_add = True)
    status = models.CharField(max_length= 20, default="active")   
    user_id = models.ForeignKey(User, on_delete= models.CASCADE, null= True)

class TemplePic(models.Model):
    temple_id = models.ForeignKey(Temple, on_delete= models.CASCADE)
    img = models.ImageField(upload_to=gallery_upload_to)
    



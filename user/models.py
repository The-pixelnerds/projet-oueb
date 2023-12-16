from django.db import models

# Create your models here.
class user(models.Model):
    username = models.CharField(max_length=30, unique=True)
    mail = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    ipadress = models.GenericIPAddressField()

class user_session(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    user_session = models.CharField(max_length=30)
    exp_date = models.DateField()
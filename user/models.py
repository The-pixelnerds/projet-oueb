from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey

class UserData(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    permissionInteger = models.IntegerField()
    colorRotation = models.IntegerField()

    def getFromUser(self, user):
        return UserData.objects.get(user=user)
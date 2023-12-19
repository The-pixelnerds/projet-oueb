from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey

class UserPermission(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    permissionInteger = models.IntegerField()

    def getFromUser(self, user):
        return UserPermission.objects.get(user=user)
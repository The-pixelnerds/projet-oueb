from django.db import models
import user.models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=30)

class RoomPermission(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(user.models.user, on_delete=models.CASCADE)
    permission = models.IntegerField()

class Permission(models.Model):
    user = models.ForeignKey(user.models.user, on_delete=models.CASCADE)
    permission = models.IntegerField()

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(user.models.user, on_delete=models.CASCADE)
    message = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)
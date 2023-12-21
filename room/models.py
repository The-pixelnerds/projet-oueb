from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    defaultPermission = models.IntegerField()
    
    def __str__(self):
        return self.name

class RoomPermission(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.IntegerField()
    
    def __str__(self):
        return self.user.username + " in " + self.room.name + " with " + str(self.permission)

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username + " in " + self.room.name + " : " + self.message
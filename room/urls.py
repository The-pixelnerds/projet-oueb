from django.urls import path
from . import views

app_name = 'room'
urlpatterns = [
    path('', views.home, name='home'),
    path('room/<int:room_id>', views.room, name='view'),
    path('create', views.createroom, name='create_room'),
    path('remove', views.removeroom, name='remove_room'),
    
    path('room/<int:room_id>/messages/<int:last_id>', views.getMessages, name='messages'),
    path('room/rooms', views.getRooms, name='rooms'),
    path('room/delete/<int:messageId>', views.removeMessage, name='delete_message')
]

from django.urls import path
from . import views

app_name = 'room'
urlpatterns = [
    path('', views.home, name='home'),
    path('room/<int:room_id>', views.room, name='view'),
    path('room/<int:room_id>/messages', views.getMessages, name='messages'),
]

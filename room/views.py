from django.shortcuts import render
from django import http
from .models import *
from user.models import *

# Create your views here.
def home(request):
    ctx = {
        'rooms': Room.objects.all(),
    }
    
    return render(request, 'room/home.html', ctx )

def room(request, room_id):
    usersess = ""
    if request.method == 'POST':
        # on recupere l'utilisateur qui a envoye le message
        user = user_session.objects.get(user_session=request.POST["tokenId"]).user
        usersess =  request.POST["tokenId"]
        
        if request.POST["message"] != "":
            #on ajoute le message
            mess = Message(room=Room.objects.get(id=room_id), user=user, message=request.POST["message"])
            mess.save()
    
    #get last message id if no message set to 0
    lastMessageId = 0
    if Message.objects.filter(room=room_id).order_by('-id').exists():
        lastMessageId = Message.objects.filter(room=room_id).order_by('-id')[0].id
    
    lastRoomId = 0
    if Room.objects.exists():
        lastRoomId = Room.objects.order_by('-id')[0].id
        
    ctx = {
        'rooms': Room.objects.all(),
        'room': Room.objects.get(id=room_id),
        'messages': Message.objects.filter(room=room_id),
        'tokenId': usersess,
        'lastMessageId': lastMessageId,
        'lastRoomId': lastRoomId
    }
    
    return render(request, 'room/view.html', ctx )

def createroom(request):
    #todo test if user have right to create room
    if request.method == 'POST':
        #on ajoute le salon
        room = Room(name=request.POST["room-name"])
        room.save()
        
        return http.HttpResponseRedirect('/channels')
    
    return render(request, 'room/creation_create.html')

def removeroom(request):
    #todo test if user have right to remove room
    if request.method == 'POST':
        #on supprime les messages du salon
        messages = Message.objects.filter(room=request.POST["room-name"])
        messages.delete()
        #on supprime le salon
        room = Room.objects.get(id=request.POST["room-name"])
        room.delete()
        
        return http.HttpResponseRedirect('/channels')
    
    ctx = {
        'rooms': Room.objects.all()
    }
    
    return render(request, 'room/creation_remove.html', ctx)

#fonction pour recup les 20 derniers messages et les renvoyer en json
def getMessages(request, room_id, last_id):
    if request.method == 'GET':
        #on recupere les derniers messages
        messages = Message.objects.filter(room=room_id, id__gt=last_id).order_by('id')
        #on les met dans un tableau
        tab = []
        for mess in messages:
            tab.append({
                'id': mess.id,
                'user': mess.user.username,
                'message': mess.message,
                'date': mess.timestamp.strftime("%d/%m/%Y %H:%M:%S")
            })
        #on renvoi le tableau en json
        return http.JsonResponse(tab, safe=False)
    else:
        return http.HttpResponseForbidden()

def getRooms(request):
    if request.method == 'GET':
        #on recupere les derniers salons
        rooms = Room.objects.filter().order_by('id')
        #on les met dans un tableau
        tab = []
        for room in rooms:
            tab.append({
                'id': room.id,
                'name': room.name
            })
        #on renvoi le tableau en json
        return http.JsonResponse(tab, safe=False)
    else:
        return http.HttpResponseForbidden()
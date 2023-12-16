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
        #on ajoute le message
        mess = Message(room=Room.objects.get(id=room_id), user=user, message=request.POST["message"])
        mess.save()
    
    #get last message id if no message set to 0
    lastMessageId = 0
    if Message.objects.filter(room=room_id).order_by('-id').exists():
        lastMessageId = Message.objects.filter(room=room_id).order_by('-id')[0].id
    
    
    ctx = {
        'rooms': Room.objects.all(),
        'room': Room.objects.get(id=room_id),
        'messages': Message.objects.filter(room=room_id),
        'tokenId': usersess,
        'lastMessageId': lastMessageId
    }
    
    return render(request, 'room/view.html', ctx )

#fonction pour recup les 20 derniers messages et les renvoyer en json
def getMessages(request, room_id):
    if request.method == 'GET':
        #on recupere les 20 derniers messages
        messages = Message.objects.filter(room=room_id).order_by('-id')[:20]
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
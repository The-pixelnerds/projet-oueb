
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import http
from tools.Perms.Perms import *

from user.models import UserData
from .models import Room, Message, RoomPermission, MessageDeletion
from django.contrib.auth.models import User

import re

# Create your views here.

@login_required
def home(request):
    rooms = Room.objects.all()
    userData = UserData.objects.get(user=request.user)
    filteredRooms = []
    for room in rooms:
        roomPerms = RoomPermission.objects.filter(room=room.id, user=request.user)
        if Perms.test(userData.permissionInteger,USER_ADMIN) or Perms.test(userData.permissionInteger,USER_ROOM_READ) or (roomPerms.exists() and Perms.test(roomPerms[0].permission, ROOM_READ)) :
            filteredRooms.append(room)
    
    ctx = {
        'rooms': filteredRooms,
        'persons': UserData.objects.all(),
    }
    
    #on ajoute ce qu'il faut pour l'affichage
    details = {
        'cancreateRoom': Perms.test(userData.permissionInteger,USER_ADMIN) or Perms.test(userData.permissionInteger, USER_ROOM_CREATE),
        'canremoveRoom': Perms.test(userData.permissionInteger,USER_ADMIN) or Perms.test(userData.permissionInteger, USER_ROOM_DELETE),
        'isadmin': Perms.test(userData.permissionInteger,USER_ADMIN),
    }
    
    ctx['details'] = details
    
    return render(request, 'room/home.html', ctx )

@login_required
def room(request, room_id):
    userData = UserData.objects.get(user=request.user)
    permInRoom = RoomPermission.objects.filter(room=room_id, user=request.user)
    
    rooms = Room.objects.all()
    filteredRooms = []
    for room in rooms:
        roomPerms = RoomPermission.objects.filter(room=room.id, user=request.user)
        if Perms.test(userData.permissionInteger,USER_ADMIN) or Perms.test(userData.permissionInteger,USER_ROOM_READ) or (roomPerms.exists() and Perms.test(roomPerms[0].permission, ROOM_READ)) :
            filteredRooms.append(room)
    
    if (Perms.test(userData.permissionInteger,USER_ADMIN) == False and Perms.test(userData.permissionInteger, ROOM_READ) == False):
        if ((not permInRoom.exists()) or ((Perms.test(permInRoom[0].permission, ROOM_ADMIN) == False and Perms.test(permInRoom[0].permission, ROOM_READ) == False))):
            print("test")
            return redirect('/channels')

    usersess = ""
    if request.method == 'POST':
        if Perms.test(userData.permissionInteger,USER_ADMIN) or Perms.test(userData.permissionInteger, USER_MESSAGE_WRITE) or (permInRoom.exists() and Perms.test(permInRoom[0].permission, ROOM_MESSAGE_WRITE)):
            # on recupere l'utilisateur qui a envoye le message
            
            if request.POST["message"] != "":
                #on ajoute le message
                mess = Message(room=Room.objects.get(id=room_id), user=request.user, message=replace_smileys(request.POST["message"]))
                mess.save()
    
    #get last message id if no message set to 0
    lastMessageId = 0
    if Message.objects.filter(room=room_id).order_by('-id').exists():
        lastMessageId = Message.objects.filter(room=room_id).order_by('-id')[0].id
    
    #just before sending the message, we remove every message that have been deleted
    if MessageDeletion.objects.filter(user=request.user).exists():
        MessageDeletion.objects.filter(user=request.user).delete()

    ctx = {}
    lastRoomId = 0
    if Room.objects.exists():
        lastRoomId = Room.objects.order_by('-id')[0].id   
        ctx = {
            'rooms': filteredRooms,
            'current_room': Room.objects.get(id=room_id),
            'room': Room.objects.get(id=room_id),
            'persons': UserData.objects.all(),
            'messages': Message.objects.filter(room=room_id),
            'lastMessageId': lastMessageId,
            'lastRoomId': lastRoomId,
            'currentuserid': request.user.id,
        }
    
    #on ajoute ce qu'il faut pour l'affichage
    details = {
        'cancreateRoom': Perms.test(userData.permissionInteger,USER_ADMIN) or Perms.test(userData.permissionInteger, USER_ROOM_CREATE),
        'canremoveRoom': Perms.test(userData.permissionInteger,USER_ADMIN) or Perms.test(userData.permissionInteger, USER_ROOM_DELETE) or (permInRoom.exists() and (Perms.test(permInRoom[0].permission, ROOM_DELETE) or Perms.test(permInRoom[0].permission, ROOM_ADMIN))),
        'canremoveMessage': Perms.test(userData.permissionInteger,USER_ADMIN) or (permInRoom.exists() and Perms.test(permInRoom[0].permission, ROOM_MESSAGE_DELETE)),
        'user': request.user,
        'isadminroom': Perms.test(userData.permissionInteger,USER_ADMIN) or (permInRoom.exists() and Perms.test(permInRoom[0].permission, ROOM_ADMIN)),
        'isadmin': Perms.test(userData.permissionInteger,USER_ADMIN),
    }
    
    ctx['details'] = details
    
    return render(request, 'room/view.html', ctx )

@login_required
def createroom(request):
    #si on a pas les droits
    if not (Perms.test(UserData.objects.get(user=request.user).permissionInteger,USER_ADMIN) or Perms.test(UserData.objects.get(user=request.user).permissionInteger, USER_ROOM_CREATE)):
        return redirect('/channels')
        
    if request.method == 'POST':
        #on ajoute le salon
        room = Room(name=request.POST["room-name"], description=request.POST["room-description"])
        
        
        #on creer le permision id du salon
        permId = 0
        permId += ROOM_MESSAGE_WRITE if request.POST.get("perm_room-message-write") else 0
        permId += ROOM_READ if request.POST.get("perm_room-read") else 0
        permId += ROOM_DELETE if request.POST.get("perm_room-delete") else 0
        permId += ROOM_ADMIN if request.POST.get("perm_room-admin") else 0
        permId += ROOM_MESSAGE_DELETE if request.POST.get("perm_room-perm_room-deleteMessage") else 0

        room.defaultPermission = permId
        room.save()

        #on ajoute les permissions du salon a tout le monde en se basant sur request.POST["room-permission"]
        for user in UserData.objects.all():
            tempP = permId
            if request.user.id == user.user.id and not Perms.test(UserData.objects.get(user=request.user).permissionInteger,USER_ADMIN):
                tempP += ROOM_ADMIN
            perm = RoomPermission(room=room, user=user.user, permission=tempP)
            perm.save()
            
        return http.HttpResponseRedirect('/channels')
    
    return render(request, 'room/creation_create.html')

@login_required
def removeroom(request):
    #todo test if user have right to remove room
    if request.method == 'POST':
        #on regarde si on a le droit de supprimer le salon
        if not (Perms.test(UserData.objects.get(user=request.user).permissionInteger,USER_ADMIN) or Perms.test(RoomPermission.objects.get(room=request.POST["room-name"], user=request.user).permission, ROOM_ADMIN)):
            return redirect('/channels/remove')

        #on supprime les permissions du salon
        perms = RoomPermission.objects.filter(room=request.POST["room-name"])
        perms.delete()
        
        #on supprime les messages du salon
        messages = Message.objects.filter(room=request.POST["room-name"])
        messages.delete()
        #on supprime le salon
        room = Room.objects.get(id=request.POST["room-name"])
        room.delete()
        
        return http.HttpResponseRedirect('/channels')
    
    #on filtre pour recuperer tout les salons où on a le droits de le supr
    rooms = Room.objects.all()
    if not Perms.test(UserData.objects.get(user=request.user).permissionInteger,USER_ADMIN) and not Perms.test(UserData.objects.get(user=request.user).permissionInteger, USER_ROOM_DELETE):
        newrooms = []
        for room in rooms:
            if Perms.test(RoomPermission.objects.get(room=room.id, user=request.user).permission, ROOM_DELETE) or Perms.test(RoomPermission.objects.get(room=room.id, user=request.user).permission, ROOM_ADMIN):
                newrooms.append(room)
        rooms = newrooms

    ctx = {
        'rooms': rooms
    }
    
    return render(request, 'room/creation_remove.html', ctx)

def editroomuserperm(request, room_id, user_id):
    #on verifie qu'on a le droit de modifier les perms du salon
    if not (Perms.test(UserData.objects.get(user=request.user).permissionInteger,USER_ADMIN) or Perms.test(RoomPermission.objects.get(room=room_id, user=request.user).permission, ROOM_ADMIN)):
        return redirect('/channels/'+str(room_id))
    
    if request.method == 'POST':
        #on recupere les perms de l'utilisateur
        perm = RoomPermission.objects.get(room=room_id, user=user_id)
        
        #on modifie les perms de l'utilisateur
        perm.permission = 0
        perm.permission += ROOM_MESSAGE_WRITE if request.POST.get("perm_room-message-write") else 0
        perm.permission += ROOM_READ if request.POST.get("perm_room-read") else 0
        perm.permission += ROOM_DELETE if request.POST.get("perm_room-delete") else 0
        perm.permission += ROOM_ADMIN if request.POST.get("perm_room-admin") else 0
        perm.permission += ROOM_MESSAGE_DELETE if request.POST.get("perm_room-deleteMessage") else 0
        perm.save()
        
        return http.HttpResponseRedirect('/channels/room/'+str(room_id))

    #on recupere les perms de l'utilisateur
    perm = RoomPermission.objects.get(room=room_id, user=user_id)

    perm_room_message_write = Perms.test(perm.permission, ROOM_MESSAGE_WRITE)
    perm_room_read = Perms.test(perm.permission, ROOM_READ)
    perm_room_delete = Perms.test(perm.permission, ROOM_DELETE)
    perm_room_admin = Perms.test(perm.permission, ROOM_ADMIN)
    perm_room_deleteMessage = Perms.test(perm.permission, ROOM_MESSAGE_DELETE)

    ctx = {
        'room': Room.objects.get(id=room_id),
        'user': UserData.objects.get(user=user_id),
        'useradmin': Perms.test(UserData.objects.get(user=request.user).permissionInteger,USER_ADMIN),
        'right_message_write': perm_room_message_write,
        'right_read': perm_room_read,
        'right_delete': perm_room_delete,
        'right_admin': perm_room_admin,
        'right_deleteMessage': perm_room_deleteMessage,
    }
    return render(request, 'room/room_user_right.html', ctx)

@login_required
def edituserperm(request, user_id):
    #on verifie qu'on a le droit de modifier les perms de l'utilisateur
    if not (Perms.test(UserData.objects.get(user=request.user).permissionInteger,USER_ADMIN)):
        return redirect('/channels')
    
    if request.method == 'POST':
        #on recupere les perms de l'utilisateur
        perm = UserData.objects.get(user=user_id)
        
        #on modifie les perms de l'utilisateur
        perm.permissionInteger = 0
        perm.permissionInteger += USER_MESSAGE_WRITE if request.POST.get("perm_user-message-write") else 0
        perm.permissionInteger += USER_ROOM_READ if request.POST.get("perm_user-read") else 0
        perm.permissionInteger += USER_ROOM_CREATE if request.POST.get("perm_user-create") else 0
        perm.permissionInteger += USER_ROOM_DELETE if request.POST.get("perm_user-delete") else 0
        perm.permissionInteger += USER_ADMIN if request.POST.get("perm_user-admin") else 0
        perm.save()
        
        return http.HttpResponseRedirect('/channels')

    #on recupere les perms de l'utilisateur
    perm = UserData.objects.get(user=user_id)

    perm_user_message_write = Perms.test(perm.permissionInteger, USER_MESSAGE_WRITE)
    perm_user_room_read = Perms.test(perm.permissionInteger, USER_ROOM_READ)
    perm_user_room_create = Perms.test(perm.permissionInteger, USER_ROOM_CREATE)
    perm_user_room_delete = Perms.test(perm.permissionInteger, USER_ROOM_DELETE)
    perm_user_admin = Perms.test(perm.permissionInteger, USER_ADMIN)

    ctx = {
        'user': UserData.objects.get(user=user_id),
        'useradmin': Perms.test(UserData.objects.get(user=request.user).permissionInteger,USER_ADMIN),
        'right_message_write': perm_user_message_write,
        'right_read': perm_user_room_read,
        'perm_user_create': perm_user_room_create,
        'right_delete': perm_user_room_delete,
        'right_admin': perm_user_admin,
    }
    return render(request, 'room/user_right.html', ctx)

@login_required
def banUser(request, userid):
    #on verifie qu'on a le droit de bannir l'utilisateur
    if not (Perms.test(UserData.objects.get(user=request.user).permissionInteger,USER_ADMIN)):
        return redirect('/channels')

    #on supprime TOUT les differentes perms de l'utilisateur de chaque salon
    perms = RoomPermission.objects.filter(user=userid)
    perms.delete()

    #on le ban (suppression de tout ses messages)
    messages = Message.objects.filter(user=userid)
    messages.delete()

    #on le supprime
    user = UserData.objects.get(user=userid)
    user.user.delete()
    user.delete()
    
    return http.HttpResponseRedirect('/channels')

#fonction pour recup les 20 derniers messages et les renvoyer en json
@login_required
def getMessages(request, room_id, last_id):
    if request.method == 'GET':
        #on recupere les derniers messages
        messages = Message.objects.filter(room=room_id, id__gt=last_id).order_by('id')
        
        #on les met dans un tableau
        tab = []
        for mess in messages:
            sanitized_message = mess.message.replace("<", "<.")
            tab.append({
                'id': mess.id,
                'user': mess.user.username,
                'message': sanitized_message,
                'date': mess.timestamp.strftime("%d/%m/%Y %H:%M:%S"),
                'candelete': Perms.test(UserData.objects.get(user=request.user).permissionInteger,USER_ADMIN) or (RoomPermission.objects.filter(room=room_id, user=request.user).exists() and (Perms.test(RoomPermission.objects.get(room=room_id, user=request.user).permission, ROOM_MESSAGE_DELETE) or Perms.test(RoomPermission.objects.get(room=room_id, user=request.user).permission, ROOM_ADMIN))),
            })
        
        #on met les messages a suprimer
        rem = []
        for mess in MessageDeletion.objects.filter(user=request.user):
            rem.append(mess.messageId)
        MessageDeletion.objects.filter(user=request.user).delete()

        #on renvoi le tableau en json
        return http.JsonResponse({'messages':tab,'deletes':rem}, safe=False)
    else:
        return http.HttpResponseForbidden()

def getRooms(request):
    if request.method == 'GET':
        #on recupere les derniers salons
        rooms = Room.objects.filter().order_by('id')
        userData = UserData.objects.get(user=request.user)
        filteredRooms = []
        for room in rooms:
            roomPerms = RoomPermission.objects.filter(room=room.id, user=request.user)
            if Perms.test(userData.permissionInteger,USER_ADMIN) or Perms.test(userData.permissionInteger,USER_ROOM_READ) or (roomPerms.exists() and Perms.test(roomPerms[0].permission, ROOM_READ)) :
                filteredRooms.append(room)
        
        #on les met dans un tableau
        tab = []
        for room in filteredRooms:
            tab.append({
                'id': room.id,
                'name': room.name
            })
        #on renvoi le tableau en json
        return http.JsonResponse(tab, safe=False)
    else:
        return http.HttpResponseForbidden()

@login_required  
def removeMessage(request,messageId):
    if request.method == 'GET':
        #on verifie qu'on a le droit de supprimer le message (admin ou auteur ou perm de suppr)
        message = Message.objects.get(id=messageId)
        userData = UserData.objects.get(user=request.user)
        permInRoom = RoomPermission.objects.filter(room=message.room.id, user=request.user)
        if not (Perms.test(userData.permissionInteger,USER_ADMIN) or message.user.id == request.user.id or (permInRoom.exists() and (Perms.test(permInRoom[0].permission, ROOM_MESSAGE_DELETE) or Perms.test(permInRoom[0].permission, ROOM_ADMIN)))):
            return http.HttpResponseForbidden()
        
        #on a le droit de supprimer le message
        #on ajoute un message de suppression a tout le monde
        for user in UserData.objects.all():
            mess = MessageDeletion(messageId=messageId, user=user.user)
            mess.save()
        
        #on supprime le message
        message.delete()

        #on dit que c'est bon
        return http.JsonResponse({'status': 'ok'})

def replace_smileys(text):
    smileys = {
        ":-)": "🙂",
        ":-(": "🙁",
        ":D": "😀",
        ":p": "😛",
        ":P": "😛",
        ":o": "😮",
        ":O": "😮",
        ":|": "😐",
        ":/": "😕",
        ";)": "😉",
        ":3": "😺",
        ":*": "😘",
    }
    for smiley, emoji in smileys.items():
        text = re.sub(re.escape(smiley), emoji, text)

    return text
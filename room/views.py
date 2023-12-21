from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import http
from tools.Perms.Perms import *

from user.models import UserData
from .models import Room, Message, RoomPermission

# Create your views here.
@login_required
def home(request):
    rooms = Room.objects.all()
    userData = UserData.objects.get(user=request.user)
    filteredRooms = []
    for room in rooms:
        roomPerms = RoomPermission.objects.filter(room=room.id, user=request.user)
        if Perms.test(userData.permissionInteger,USER_ADMIN) or (roomPerms.exists() and Perms.test(roomPerms[0].permission, ROOM_READ)) :
            filteredRooms.append(room)
    
    ctx = {
        'rooms': filteredRooms,
        'persons': UserData.objects.all()
    }
    
    #on ajoute ce qu'il faut pour l'affichage
    details = {
        'cancreateRoom': Perms.test(userData.permissionInteger,USER_ADMIN) or Perms.test(userData.permissionInteger, USER_ROOM_CREATE),
        'canremoveRoom': Perms.test(userData.permissionInteger,USER_ADMIN) or Perms.test(userData.permissionInteger, USER_ROOM_DELETE),
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
        if Perms.test(userData.permissionInteger,USER_ADMIN) or (roomPerms.exists() and Perms.test(roomPerms[0].permission, ROOM_READ)) :
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
                mess = Message(room=Room.objects.get(id=room_id), user=request.user, message=request.POST["message"])
                mess.save()
    
    #get last message id if no message set to 0
    lastMessageId = 0
    if Message.objects.filter(room=room_id).order_by('-id').exists():
        lastMessageId = Message.objects.filter(room=room_id).order_by('-id')[0].id
    
    ctx = {}
    lastRoomId = 0
    if Room.objects.exists():
        lastRoomId = Room.objects.order_by('-id')[0].id   
        ctx = {
            'rooms': filteredRooms,
            'room': Room.objects.get(id=room_id),
            'persons': UserData.objects.all(),
            'messages': Message.objects.filter(room=room_id),
            'lastMessageId': lastMessageId,
            'lastRoomId': lastRoomId,
        }
    
    #on ajoute ce qu'il faut pour l'affichage
    details = {
        'cancreateRoom': Perms.test(userData.permissionInteger,USER_ADMIN) or Perms.test(userData.permissionInteger, USER_ROOM_CREATE),
        'canremoveRoom': Perms.test(userData.permissionInteger,USER_ADMIN) or Perms.test(userData.permissionInteger, USER_ROOM_DELETE),
    }
    
    ctx['details'] = details
    
    return render(request, 'room/view.html', ctx )

@login_required
def createroom(request):
    #si on a pas les droits
    if not Perms.test(UserData.objects.get(user=request.user).permissionInteger,USER_ADMIN) or Perms.test(UserData.objects.get(user=request.user).permissionInteger, USER_ROOM_CREATE):
        return redirect('/channels')
        
    if request.method == 'POST':
        #on ajoute le salon
        room = Room(name=request.POST["room-name"], description=request.POST["room-description"])
        
        perms = request.POST.get("perms") if request.POST.get("perms") != None else []
        #on creer le permision id du salon
        permId = 0
        permId += ROOM_MESSAGE_WRITE if "perm_room-message-write" in perms else 0
        permId += ROOM_READ if "perm_room-read" in perms else 0
        permId += ROOM_DELETE if "perm_room-delete" in perms else 0
        permId += ROOM_ADMIN if "perm_room-admin" in perms else 0
        
        print(permId)
        room.defaultPermission = permId
        room.save()

        #on ajoute les permissions du salon a tout le monde en se basant sur request.POST["room-permission"]
        for user in UserData.objects.all():
            tempP = permId
            if request.user.id == user.user.id and not "perm_room-admin" in perms:
                tempP += ROOM_ADMIN
            perm = RoomPermission(room=room, user=user.user, permission=tempP)
            perm.save()
            
        return http.HttpResponseRedirect('/channels')
    
    return render(request, 'room/creation_create.html')

@login_required
def removeroom(request):
    if not Perms.test(UserData.objects.get(user=request.user).permissionInteger,USER_ADMIN) or Perms.test(UserData.objects.get(user=request.user).permissionInteger, USER_ROOM_DELETE):
        return redirect('/channels')
    #todo test if user have right to remove room
    if request.method == 'POST':
        #on regarde si on a le droit de supprimer le salon
        if not Perms.test(UserData.objects.get(user=request.user).permissionInteger,USER_ADMIN) or Perms.test(RoomPermission.objects.get(room=request.POST["room-name"], user=request.user).permission, ROOM_ADMIN):
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
        userData = UserData.objects.get(user=request.user)
        filteredRooms = []
        for room in rooms:
            roomPerms = RoomPermission.objects.filter(room=room.id, user=request.user)
            if Perms.test(userData.permissionInteger,USER_ADMIN) or (roomPerms.exists() and Perms.test(roomPerms[0].permission, ROOM_READ)) :
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
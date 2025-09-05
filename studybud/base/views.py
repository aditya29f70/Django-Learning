from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.

# rooms= [
#     {'id':1, 'name':'Lets learn python!'},
#     {'id':2, 'name':'Design with me'},
#     {'id':3, 'name':'Frontend Developers'}
# ]


def loginPage(request):
    if request.method== 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
    # now try to check is this user exist or not 
        try:
            user= User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
# if user exist then we have to authenticate()
        user= authenticate(request, username= username, password= password)
    # here we will get user obj base on there authentication result
    # now what authent.. gonna do, either  gives us an error or return an user object
    # which matches these credencials (like each thing username and password have there own creadencial)

    # if user is good or pass there credencial then it is good to login
        if user is not None:
            login(request, user)
        # what login does it add this user session(user info) in the database and inside our browser
        # so user offical loged in 
            return redirect('home')
        else:
            messages.error(request, 'Username Or password does not exist.')

    context= {}
    return render(request, 'base/login_register.html', context)



def home(request):
    q= request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms= Room.objects.filter(
        Q(topic__name__icontains= q) |
        Q(name__icontains=q) |
        Q(desciption__icontains=q)
    )
    # rooms= Room.objects.all()
    topics= Topic.objects.all()
    room_count= rooms.count()
    context= {'room':rooms, 'topic':topics, 'room_count':room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id= pk)
    context= {'room': room}
    return render(request, 'base/room.html', context)


def createRoom(request):
    form = RoomForm()
    if request.method== 'POST':
        # request.POST.get('name')
        form = RoomForm(request.POST)
        if form.is_valid():
            # like this is for if your all the request.post value is good according there correcspoing value 
            # then save it --> so then will save that value in the database
            form.save()
            return redirect('home')
    context={'form': form }
    return render(request, 'base/room_form.html',context )

def updateRoom(request, pk):
    room= Room.objects.get(id= pk)
    form= RoomForm(instance=room)
    if request.method== 'POST':
        form= RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context= {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room= Room.objects.get(id= pk)
    if request.method== 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {"obj":room})
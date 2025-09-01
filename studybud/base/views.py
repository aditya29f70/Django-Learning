from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.

# rooms= [
#     {'id':1, 'name':'Lets learn python!'},
#     {'id':2, 'name':'Design with me'},
#     {'id':3, 'name':'Frontend Developers'}
# ]






def home(request):
    q= request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms= Room.objects.filter(topic__name__icontains= q) 
    # rooms= Room.objects.all()
    topics= Topic.objects.all()
    context= {'room':rooms, 'topic':topics}
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
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from .models import RoomRating, Room
from .forms import CreateForm
def index(request):
	context = {}
	return render(request, 'comfort/home.html', context)

def detailIndex(request):

	ratings_list = RoomRating.objects.all()
	context = {'ratings_list': ratings_list}
	
	return render(request, 'comfort/detailIndex.html', context)

def detail(request, room_rating_id):
	rating = RoomRating.objects.get(pk=room_rating_id)
	context = {'rating': rating.rating, 'room_rating': rating}
	return render(request, 'comfort/detail.html', context)

def create(request):
	rooms = Room.objects.all()
	
	context = {}
	if request.method == "POST":
		
		print(request.POST['room'])
		form = CreateForm()
		context = {'rooms': rooms, 'form': form}
		return render(request, 'comfort/create.html', context)

	else:
		
		form = CreateForm()
		context = {'rooms': rooms, 'form': form}
		return render(request, 'comfort/create.html', context)

def login(request):

	context = {}

	return render(request, 'comfort/auth.php', context)

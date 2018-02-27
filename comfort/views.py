# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from .models import RoomRating, Room
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
	context = {'rooms': rooms}
	return render(request, 'comfort/create.html', context)

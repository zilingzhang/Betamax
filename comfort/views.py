# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse

import time, paramiko

from .models import RoomRating, Room
from .forms import CreateForm, RoomUpdateForm
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
		
		room = Room.objects.get(id=request.POST['room'])
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		#Above is not very secure, recomend change
		ssh.connect('138.67.198.23',22,'hcr','HCR')
		stdin, stdout, stderr = ssh.exec_command('pwd')
		#print(stdin)
		print(stdout.read())
		#print(stderr)
		#TODO:  run scripts to create the association tables for a new rating, raise error if unable to connect to turtlebot
		return redirect('detail', 1);

	else:
		
		form = CreateForm()
		context = {'rooms': rooms, 'form': form}
		return render(request, 'comfort/create.html', context)

def login(request):

	context = {}

	return render(request, 'registration/login.html', context)

def config(request):
	msg = ""
	if request.method == "POST":
		print(request.POST)
		room = Room.objects.get(id=request.POST['room'])
		print(room.active)
		if 'active' in request.POST:
			room.active = True
		else:
			room.active = False
		room.save()
		msg = "Room successfully updated!"

	form = RoomUpdateForm()
	rooms = Room.objects.all()
	context = {'rooms': rooms, 'form': form, 'msg': msg}


	return render(request, 'comfort/config.html', context)

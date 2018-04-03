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
		
		ssh2 = paramiko.SSHClient()
		ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		# ssh = paramiko.SSHClient()
		# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		# #Above is not very secure, recomend change
		# ssh.connect('138.67.196.184',22,'hcr','HCR')
		# stdin, stdout, stderr = ssh.exec_command('roslaunch turtlebot_bringup minimal.launch')
		# ssh3 = paramiko.SSHClient()
		# ssh3.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		# #Above is not very secure, recomend change
		# ssh3.connect('138.67.196.184',22,'hcr','HCR')
		# stdin3, stdout3, stderr3 = ssh3.exec_command('roslaunch turtlebot_navigation amcl_demo.launch map_file:=/home/hcr/maps/betterfrontroom.yaml')
		# while(stdout3.read()!="ODOM RECEIVED"):
		# 	print(stdout3.read())
		ssh2.connect('138.67.196.184',22,'hcr','HCR')
		
		stdin2, stdout2, stderr2 = ssh2.exec_command('python helloworld/turtlebot/movement_algo.py')
		#print(stdin)
		print(stdout2.read())
		print(stderr2.read())
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

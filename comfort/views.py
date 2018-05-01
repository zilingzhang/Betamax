# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

import time, paramiko, subprocess

from .models import RoomRating, Room, Rating
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
	#subprocess.check_output('/scripts/ComfortRobot.exe')
	context = {'rating': rating.rating, 'room_rating': rating}
	return render(request, 'comfort/detail.html', context)

@login_required
def create(request):
	rooms = Room.objects.all()
	
	context = {}
	if request.method == "POST":
		
		room = Room.objects.get(id=request.POST['room'])
		file = ""
		
		ssh2 = paramiko.SSHClient()
		ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh2.connect('138.67.205.169',22,'hcr','HCR')
	
		stdin2, stdout2, stderr2 = ssh2.exec_command(command='echo $PYTHONPATH',bufsize=-1,timeout=None,get_pty=True)
		#DOES NOT WORK, PATH on parimiko object does not include ros libraries, errors out when trying to run script
		#stdin2, stdout2, stderr2 = ssh2.exec_command('pwd')
		#print(stdin)
		# chan=ssh2.invoke_shell()
		# chan.send('echo $PATH')
		# print(chan.recv(1024))
		test = stdout2.read()
		print(test)
		print(stderr2.read())
		#rate = Rating(ave_light=light,ave_ambient_temp=ambtemp, ave_radiant_temp=radtemp, \
			#ave_humidity=hum, ave_x_airflow=xflow, ave_y_airflow=yflow, csvfile=file)
		#stdin2, stdout2, stderr2 = ssh2.exec_command('scp hcr@stuff:path static/csvs/')
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


@login_required
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

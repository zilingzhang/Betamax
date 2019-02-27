# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Rating(models.Model):
	
	value = models.FloatField()
	ave_light = models.FloatField()
	ave_ambient_temp = models.FloatField()
	ave_radiant_temp = models.FloatField()
	ave_humidity = models.FloatField()
	ave_x_airflow = models.FloatField()
	ave_z_airflow = models.FloatField()
	ave_sound_level = models.FloatField()
	csvfile = models.FileField(upload_to='static/csvs/', null=True)

	def __str__(self):
		return str(self.value)


class Room(models.Model):
	BUILDING_CHOICES = (
		('BB', 'Brown'),
		('MZ', 'Marquez'),
		('SH', 'Stratton'),
	)

	roomscript = models.CharField(max_length=1000, default="")
	building = models.CharField(max_length=2, choices=BUILDING_CHOICES)
	roomnumber = models.IntegerField()
	active = models.BooleanField(default=True)

	def __str__(self):
		return (self.building+ ' '+ str(self.roomnumber))

class RoomRating(models.Model):

	rating = models.ForeignKey(Rating,on_delete=models.PROTECT)
	room = models.ForeignKey(Room,on_delete=models.PROTECT)
	date = models.DateTimeField('Date Measured')

	def __str__(self):
		return str(self.room) + ' '+ str(self.date.month)+ '/'+ str(self.date.day)+ '/' \
		+ str(self.date.year)






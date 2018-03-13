# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Measurement(models.Model):

	rating = models.FloatField()
	light = models.FloatField()
	ambient_temp = models.FloatField()
	radiant_temp = models.FloatField()
	humidity = models.FloatField()
	x_airflow = models.FloatField()
	z_airflow = models.FloatField()
	sound_level = models.FloatField()
	x_pos = models.FloatField()
	y_pos = models.FloatField()

	def __str__(self):
		return str(self.rating)

class Rating(models.Model):
	
	value = models.FloatField()
	ave_light = models.FloatField()
	ave_ambient_temp = models.FloatField()
	ave_radiant_temp = models.FloatField()
	ave_humidity = models.FloatField()
	ave_x_airflow = models.FloatField()
	ave_z_airflow = models.FloatField()
	ave_sound_level = models.FloatField()

	def __str__(self):
		return str(self.value)

class RatingMeasurement(models.Model):
	rating = models.ForeignKey(Rating)
	measurement = models.ForeignKey(Measurement)


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

	rating = models.ForeignKey(Rating)
	room = models.ForeignKey(Room)
	date = models.DateTimeField('Date Measured')

	def __str__(self):
		return str(self.room) + ' '+ str(self.date.month)+ '/'+ str(self.date.day)+ '/' \
		+ str(self.date.year)






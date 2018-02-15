# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Rating, Room, RoomRating

# Register your models here.
admin.site.register(Rating)
admin.site.register(Room)
admin.site.register(RoomRating)
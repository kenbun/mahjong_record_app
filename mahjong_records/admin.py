# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import User, Game, Record

admin.site.register(User)
admin.site.register(Game)
admin.site.register(Record)

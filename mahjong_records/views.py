# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.db import models
from .models import User, Record, Game
import datetime, operator

def index(request):
  today = datetime.date.today()
  game = Game.objects.filter(playing_date__date=today)
  template = loader.get_template('mahjong_records/index.html')
  context = {
    'game':game,
  }
  return HttpResponse(template.render(context, request))

def total(request):
  today = datetime.date.today()
  game = Game.objects.filter(playing_date__date=today)
  users = User.objects.filter(record__game__playing_date__date=today).distinct()
  user_data = [{'name':user.name} for user in users]
  for i, user in enumerate(users):
    user_data[i].update(user.record_set.filter(game__playing_date__date=today).aggregate(sum_point=models.Sum('point'),ave_rank=models.Avg('rank')))
  template = loader.get_template('mahjong_records/total.html')
  context = {
    'game':game,
    'stats':sorted(user_data, key=operator.itemgetter('sum_point'), reverse=True),
  }
  return HttpResponse(template.render(context, request))

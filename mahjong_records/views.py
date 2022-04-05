# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.db import models
from .models import User, Record, Game
import datetime, operator, logging

def index(request):
  today = datetime.date.today()
  game = Game.objects.filter(playing_date__date=today).order_by("-playing_date")
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

def career(request):
  users = User.objects.all()
  user_data = [{'name':user.name} for user in users]
  for i, user in enumerate(users):
    user_data[i].update(user.record_set.aggregate(sum_point=models.Sum('point'),ave_rank=models.Avg('rank'),max_score=models.Max('score'),ave_score=models.Avg('score'), count_match=models.Count('rank')))
  template = loader.get_template('mahjong_records/career.html')
  context = {
    'stats':sorted(user_data, key=operator.itemgetter('sum_point'), reverse=True),
  }
  return HttpResponse(template.render(context, request))

def record_match(request):
  users = User.objects.all()
  home = {"east":"東家", "south":"南家", "west":"西家", "north":"北家"}

  return render(request, 'mahjong_records/record_match.html', {'users':users, 'home':home,})

def resister_match(request):
  users = User.objects.all()
  home = {"east":"東家", "south":"南家", "west":"西家", "north":"北家"}
  user_score = {}
  uma_oka = [50.0, 10.0, -10.0, -30.0]
  temp = []

  for player in home:
    user_score[request.POST[player]] = int(request.POST[player+'_score'])

  if (sum(user_score.values())!=(250*4)) or (0 in user_score) or (len(user_score) != len(set(user_score))):
    return render(request, 'mahjong_records/record_match.html', {
      'users':users, 
      'home':home,
      'error_message':"正しく入力してください",
      'request':request
      })
  else:
    today = datetime.datetime.today()
    game = Game.objects.create(playing_date=today)
    for i, userid_score in enumerate(sorted(user_score.items(), key=lambda x:x[1], reverse=True)):
      user_score = userid_score[1]*100
      user_point = float(user_score/1000)+uma_oka[i]-30.0
      print(user_score, user_point)
      Record.objects.create(rank=i+1, score=user_score, point=user_point, user=users.get(id=userid_score[0]), game=game)

    return render(request, 'mahjong_records/resister_match.html')



# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.db import models
from .models import User, Record, Game
import datetime, operator, logging
import numpy as np

def index(request):
  today = datetime.date.today()
  game = Game.objects.filter(playing_date__date=today).order_by("-playing_date")
  template = loader.get_template('mahjong_records/index.html')
  context = {
    'game':game,
  }
  return render(request, 'mahjong_records/index.html', context)

def total(request):
  today = datetime.date.today()
  game = Game.objects.filter(playing_date__date=today)
  users = User.objects.filter(record__game__playing_date__date=today).distinct()
  user_data = [{'name':user.name, 'id':user.id} for user in users]
  for i, user in enumerate(users):
    user_data[i].update(user.record_set.filter(game__playing_date__date=today).aggregate(sum_point=models.Sum('point'),ave_rank=models.Avg('rank'),max_score=models.Max('score'),ave_score=models.Avg('score'), count_match=models.Count('rank')))
    today_records = user.record_set.filter(game__playing_date__date=today)
    counts = today_records.count()
    top = today_records.filter(rank=1).count()
    worst = today_records.filter(rank=4).count()
    user_data[i].update({"top_rate":float(top/counts), "avoid_worst_rate":1-float(worst/counts)})
  template = loader.get_template('mahjong_records/total.html')
  context = {
    'game':game,
    'stats':sorted(user_data, key=operator.itemgetter('sum_point'), reverse=True),
  }
  return render(request, 'mahjong_records/total.html', context)

def career(request):
  users = User.objects.all()
  user_data = [{'name':user.name, 'id':user.id} for user in users]
  for i, user in enumerate(users):
    if user.record_set.count() > 0:
      user_data[i].update(user.record_set.aggregate(sum_point=models.Sum('point'),ave_rank=models.Avg('rank'),max_score=models.Max('score'),ave_score=models.Avg('score'), count_match=models.Count('rank')))
      counts = user.record_set.count()
      top = user.record_set.filter(rank=1).count()
      worst = user.record_set.filter(rank=4).count()
      user_data[i].update({"top_rate":float(top/counts), "avoid_worst_rate":1-float(worst/counts)})
    else:
      user_data[i].update({"sum_point":0,"ave_rank":0,"max_score":0,"ave_score":0, "count_match":0, "top_rate":0, "avoid_worst_rate":0})
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
    arr = np.array(list(user_score.values()))
    u,inv,k=np.unique(-np.sort(arr)[::-1], return_inverse=True, return_counts=True)
    for i, userid_score in enumerate(sorted(user_score.items(), key=lambda x:x[1], reverse=True)):
      user_score = userid_score[1]*100
      rank=k[:inv[i]].sum()+1
      user_point = float(user_score/1000)+uma_oka[rank-1]/k[inv[i]]-30.0
      Record.objects.create(rank=rank, score=user_score, point=user_point, user=users.get(id=userid_score[0]), game=game)

    return render(request, 'mahjong_records/resister_success.html', {'message':"対局結果を記録しました."})

def record_user(request):
   return render(request, 'mahjong_records/record_user.html')

def resister_user(request):
  today = datetime.datetime.today()
  user = User.objects.create(name=request.POST["name"], created_at=today)
  return render(request, 'mahjong_records/resister_success.html', {'message':"プレイヤー登録を完了しました."})

def user_detail(request, user_id):
  user = User.objects.get(id=user_id)
  if user.record_set.count() > 0:
    records = user.record_set.all().order_by("-game__playing_date")
    stats = user.record_set.aggregate(sum_point=models.Sum('point'),ave_rank=models.Avg('rank'),max_score=models.Max('score'),ave_score=models.Avg('score'), count_match=models.Count('rank'))
    counts = user.record_set.count()
    top = user.record_set.filter(rank=1).count()
    worst = user.record_set.filter(rank=4).count()
    stats.update({"top_rate":float(top/counts), "avoid_worst_rate":1-float(worst/counts)})
  return render(request, 'mahjong_records/user_detail.html', {'user':user, 'stats':stats, 'records':records})

def game_detail(request, game_id):
  game = Game.objects.get(id=game_id)
  records = game.record_set.all().order_by("rank")
  return render(request, 'mahjong_records/game_detail.html', {'records':records})
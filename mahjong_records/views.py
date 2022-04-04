# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import User, Record, Game
import datetime

def index(request):
  today = datetime.date.today()
  game = Game.objects.filter(playing_date__date=today)
  template = loader.get_template('mahjong_records/index.html')
  context = {
    'game':game,
  }
  return HttpResponse(template.render(context, request))

# def total(request):
#   today = datetime.date.today()
#   users = User.objects.filter(userrecord__record__gamerecord__game__playing_date__date=today).distinct()
#   template = loader.get_template('mahjong_records/total.html')
#   context = {
#     'users':users,
#   }
#   return HttpResponse(template.render(context, request))
  

# def game(request, game_id):
#   game = Game.objects.get(id=game_id)
#   users = [User.objects.get(id=user.id) for user in UserRecord.objects.filter(game_id=game.id)]
#   return HttpResponse("game_id:{}, users:{},{},{},{}".format(game.id, users[0].name, users[1].name, users[2].name,users[3].name))  
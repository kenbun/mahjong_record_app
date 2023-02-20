# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
  name = models.CharField(verbose_name='名前', max_length=32)
  created_at = models.DateTimeField(verbose_name='作成日時')

  def __str__(self):
    return self.name

class Game(models.Model):
  playing_date = models.DateTimeField(verbose_name='ゲーム開催日時')
  def __str__(self):
    return timezone.localtime(self.playing_date).strftime("%Y/%m/%d %H:%M")

  def users(self):
    users = self.record_set.all().order_by("rank")
    return users

class Record(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user_id')
  game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='game_id')
  rank = models.IntegerField(default=1)
  score = models.IntegerField(default=25000)
  point = models.FloatField(default=0)

  def __str__(self):
    return str(self.rank)+"着,"+self.user.name+str(self.point)+timezone.localtime(self.game.playing_date).strftime("%Y/%m/%d %H:%M")


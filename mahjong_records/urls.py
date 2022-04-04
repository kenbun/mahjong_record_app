from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('total/', views.total, name="total"),
    # path('<int:game_id>/game/', views.game, name="game"),
]
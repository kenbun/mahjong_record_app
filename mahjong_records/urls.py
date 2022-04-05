from django.urls import path

from . import views

app_name="mahjong_records"

urlpatterns = [
    path('', views.index, name='index'),
    path('total/', views.total, name="total"),
    path('career/', views.career, name="career"),
    path('record_match/', views.record_match, name="record_match"),
    path('resister_match/', views.resister_match, name="resister_match"),
    path('record_user/', views.record_user, name="record_user"),
    path('resister_user/', views.resister_user, name="resister_user"),
]
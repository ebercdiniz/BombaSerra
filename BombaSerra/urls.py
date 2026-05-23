from django.contrib import admin
from django.urls import path

from Bombas import views

urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),

    path('api/state/', views.get_state, name='api_state'),

    path('api/set_mode/', views.set_mode, name='api_set_mode'),

    path('api/espstate/', views.esp32_state, name='api_espstate'),

    path('api/add_schedule/', views.add_schedule, name='add_schedule'),

    path('api/delete_schedule/', views.delete_schedule, name='delete_schedule'),
]
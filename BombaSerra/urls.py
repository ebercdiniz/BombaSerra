"""
URL configuration for BombaSerra project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.urls import path
from Bombas import views

urlpatterns = [
    # Página principal (TemplateView)
    path('', views.IndexView.as_view(), name='index'),

    # APIs para o ESP32
    path('api/state/', views.get_state, name='api_state'),
    path('api/set_mode/', views.set_mode, name='api_set_mode'),
    path('api/espstate/', views.esp32_state, name='api_espstate'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('process/', views.process_weather_data, name='process_weather'),
]


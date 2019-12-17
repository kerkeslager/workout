from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('settings/', views.settings, name='settings'),
]

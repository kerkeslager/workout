from django.urls import path

from . import api_views

app_name = 'api:program'

urlpatterns = [
    path('', api_views.program, name='program'),
]

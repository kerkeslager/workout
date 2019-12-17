from django.urls import path

from . import api_views

urlpatterns = [
    path('workout/recommend/', api_views.workout_recommend, name='workout'),
]

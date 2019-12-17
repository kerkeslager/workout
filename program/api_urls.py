from django.urls import path

from . import api_views

urlpatterns = [
    path('workout/', api_views.workout_list, name='workout'),
]

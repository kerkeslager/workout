from django.urls import path

from . import api_views

urlpatterns = [
    path('workout-record/start/', api_views.start_workout_record, name='start_workout_record'),
    path('workout-record/finish/', api_views.finish_workout_record, name='finish_workout_record'),
    path('set-record/update/', api_views.update_set_record, name='update_set_record'),
]

from django.http import JsonResponse

from . import models
from user import models as user_models

def _serialize_program_workout(workout, user):
    return {
        'id': workout.identifier,
        'name': workout.name,
        'ongoing': workout.ongoing_for_user(user),
        'exercises': [
            {
                'id': workout_exercise.exercise.identifier,
                'name': workout_exercise.exercise.name,
                'weight': workout_exercise.weight,
                'workSets': [ workout_exercise.reps for ignore in range(workout_exercise.sets) ],
            }
            for workout_exercise in workout.exercises.through.objects.filter(workout=workout)
        ]
    }

def workout_recommend(request):
    program_workouts = [
        program_workout
        for program in request.user.profile.programs.all()
        for program_workout in program.workouts.all()
    ]

    recommended = list(request.user.profile.get_recommended_program_workouts())
    other = [pw for pw in program_workouts if pw not in recommended]

    result = {
        'recommended': [
            _serialize_program_workout(program_workout, request.user)
            for program_workout in recommended
        ],
        'other': [
            _serialize_program_workout(program_workout, request.user)
            for program_workout in other
        ],
    }

    return JsonResponse(result)

from django.http import JsonResponse

from . import models

def workout_list(request):
    workouts = (
        workout
        for program in request.user.profile.programs.all()
        for workout in program.workouts.all()
    )

    result = {
        'workouts': [
            {
                'identifier': workout.identifier,
                'name': workout.name,
                'exercises': [
                    {
                        'identifier': workout_exercise.exercise.identifier,
                        'name': workout_exercise.exercise.name,
                        'weight': workout_exercise.weight,
                        'workSets': [ workout_exercise.reps for ignore in range(workout_exercise.sets) ],
                    }
                    for workout_exercise in workout.exercises.through.objects.filter(workout=workout)
                ]
            }
            for workout in workouts
        ],
    }

    return JsonResponse(result)

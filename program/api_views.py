from django.http import JsonResponse

from . import models

def program(request):
    my_program = request.user.profile.programs.all().first()

    result = {
        'name': my_program.name,
        'workouts': [
            {
                'name': workout.name,
                'exercises': [
                    {
                        'name': workout_exercise.exercise.name,
                        'weight': workout_exercise.weight,
                        'workSets': [ workout_exercise.reps for ignore in range(workout_exercise.sets) ],
                    }
                    for workout_exercise in workout.exercises.through.objects.filter(workout=workout)
                ]
            }
            for workout in my_program.workouts.all()
        ],
    }

    return JsonResponse(result)

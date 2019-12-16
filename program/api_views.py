from django.http import JsonResponse

from . import models

def program(request):
    my_program = models.Program.objects.all()[0]

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
            for workout in my_program.workout_set.all()
        ],
    }

    return JsonResponse(result)

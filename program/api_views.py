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
                        'name': exercise.name,
                        'weight': exercise.weight,
                        'workSets': [ exercise.reps for ignore in range(exercise.sets) ],
                    }
                    for exercise in workout.exercise_set.all()
                ]
            }
            for workout in my_program.workout_set.all()
        ],
    }

    return JsonResponse(result)

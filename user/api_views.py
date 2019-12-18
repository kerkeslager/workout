import json

from django.http import JsonResponse

from . import models
from program import models as program_models

def _serialize_workout_record(workout_record):
    return {
        'id': workout_record.identifier,
        'complete': workout_record.is_finished,
        'name': workout_record.program_workout.name,
        'exercises': [
            {
                'id': exercise_record.identifier,
                'name': exercise_record.exercise.name,
                'weight': exercise_record.planned_weight,
                'workSets': [
                    {
                        'id': set_record.identifier,
                        'plannedReps': set_record.planned_reps,
                        'completedReps': set_record.completed_reps,
                    }
                    for set_record in exercise_record.set_records.all()
                ],
            }
            for exercise_record in workout_record.exercise_records.all()
        ],
    }

def start_workout_record(request):
    assert request.method == 'POST'
    payload = json.loads(request.body)
    program_workout_identifier = payload['programWorkout']

    program_workout = program_models.ProgramWorkout.objects.get(
        identifier=program_workout_identifier,
    )

    workout_record = models.WorkoutRecord.objects.filter(
        user=request.user,
        program_workout=program_workout,
        is_finished=False,
    ).first()

    if workout_record:
        return JsonResponse(_serialize_workout_record(workout_record))

    workout_record = models.WorkoutRecord(
        user=request.user,
        program_workout=program_workout,
    )
    workout_record.save()

    for program_exercise in program_workout.program_exercises.all():
        exercise_record = models.ExerciseRecord(
            user=request.user,
            exercise=program_exercise.exercise,
            workout_record=workout_record,
            planned_weight=program_exercise.weight,
        )
        exercise_record.save()

        for s in range(program_exercise.sets):
            set_record = models.SetRecord(
                exercise_record=exercise_record,
                planned_reps=program_exercise.reps,
            )
            set_record.save()

    return JsonResponse(_serialize_workout_record(workout_record))

def finish_workout_record(request):
    assert request.method == 'POST'
    payload = json.loads(request.body)
    workout_record_identifier = payload['workoutRecord']

    workout_records = models.WorkoutRecord.objects.filter(
        identifier=workout_record_identifier,
        user=request.user,
    )

    if workout_records.count() == 0:
        return JsonResponse({
            'success': False,
            'message': 'No WorkoutRecord found with this ID.',
        }, status=404)

    assert workout_records.count() == 1

    workout_records.update(is_finished=True)

    return JsonResponse({
        'success': True,
    })

def update_set_record(request):
    assert request.method == 'POST'
    payload = json.loads(request.body)
    set_record_identifier = payload.pop('setRecord', None)

    if not set_record_identifier:
        return JsonResponse({
            'success': False,
            'message': 'Parameter "setRecord" is required',
        })

    set_records = models.SetRecord.objects.filter(
        identifier=set_record_identifier,
        exercise_record__user=request.user,
    )

    if set_records.count() == 0:
        return JsonResponse({
            'success': False,
            'message': 'No SetRecord found with this ID.',
        }, status=404)

    assert set_records.count() == 1

    updates = {}

    for key in payload.keys():
        if key == 'completedReps':
            if payload['completedReps'] is None:
                updates['completed_reps'] = None

            else:
                updates['completed_reps'] = int(payload['completedReps'])

        else:
            return JsonResponse({
                'success': False,
                'message': 'Unexpected field "{}"'.format(key),
            }, status=400)

    if not updates:
        return JsonResponse({
            'success': False,
            'message': 'At least 1 field to update is required. Allowed fields: {}'.format(
                ', '.join('"{}"'.format(f) for f in ['completedReps']),
            ),
        })

    set_records.update(**updates)

    return JsonResponse({
        'success': True,
    })

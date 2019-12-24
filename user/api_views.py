import datetime
import json

from django.db import transaction
from django.http import JsonResponse

from . import models
from base import utils
from program import models as program_models

def _serialize_set_record(set_record):
    return {
        'id': set_record.identifier,
        'plannedReps': set_record.planned_reps,
        'completedReps': set_record.completed_reps,
        'weight': set_record.weight,
    }

def _serialize_exercise_record(exercise_record):
    return {
        'id': exercise_record.identifier,
        'name': exercise_record.exercise.name,
        'weight': exercise_record.planned_weight,
        'warmupSets': [
            _serialize_set_record(set_record)
            for set_record in exercise_record.warmup_set_records.all()
        ],
        'workSets': [
            _serialize_set_record(set_record)
            for set_record in exercise_record.work_set_records.all()
        ],
    }

def _serialize_workout_record(workout_record):
    return {
        'id': workout_record.identifier,
        'complete': workout_record.is_finished,
        'name': workout_record.program_workout.name,
        'exercises': [
            _serialize_exercise_record(exercise_record)
            for exercise_record in workout_record.exercise_records.all()
        ],
    }

def _get_planned_weight_for_user(program_exercise, user):
    previous_exercise_records = models.ExerciseRecord.objects.filter(
        user=user,
        exercise=program_exercise.exercise,
    ).order_by('-created')

    failed_counter = 0
    last_successful_record = None

    for previous_exercise_record in previous_exercise_records:
        if previous_exercise_record.succeeded:
            last_successful_record = previous_exercise_record
            break
        else:
            failed_counter += 1

    if not last_successful_record:
        return program_exercise.start_weight

    # Deload if we've failed 3 times
    if failed_counter >= 3:
        return max(
            program_exercise.start_weight,
            utils.round_to_nearest(last_successful_record.planned_weight * 4 / 5, 5),
        )

    # Deload 20% for every two weeks since we last did this
    last_record = previous_exercise_records.first()
    if last_record.created < (utils.utcnow() - datetime.timedelta(days=14)):
        days_since_last_record = (utils.utcnow() - last_record.created).days
        two_week_periods = days_since_last_record // 14
        cumulative_factor = 4**two_week_periods / 5**two_week_periods
        return max(
            program_exercise.start_weight,
            round_to_nearest(
                last_successful_record.planned_weight * cumulative_factor,
                5,
            ),
        )

    return last_successful_record.planned_weight + 5

def _generate_set_records(exercise_record, program_exercise=None):
    if program_exercise is None:
        program_exercise = exercise_record.workout_record.program_workout.program_exercises.filter(
            exercise=exercise_record.exercise,
        ).first()

    planned_weight = exercise_record.planned_weight

    if planned_weight * 75 / 100 > program_exercise.start_weight:
        set_record = models.SetRecord(
            exercise_record=exercise_record,
            planned_reps=program_exercise.reps,
            weight=program_exercise.start_weight,
            is_work_set=False,
        )
        set_record.save()

    for percent in (45, 65, 75, 85):
        if planned_weight * (percent - 25) / 100 > program_exercise.start_weight:
            weight = utils.round_to_nearest(planned_weight * percent / 100, 5)

            set_record = models.SetRecord(
                exercise_record=exercise_record,
                planned_reps=program_exercise.reps,
                weight=weight,
                is_work_set=False,
            )
            set_record.save()

    for s in range(program_exercise.sets):
        set_record = models.SetRecord(
            exercise_record=exercise_record,
            planned_reps=program_exercise.reps,
            weight=exercise_record.planned_weight,
            is_work_set=True,
        )
        set_record.save()

@transaction.atomic
def update_exercise_record(request):
    assert request.method == 'POST'
    payload = json.loads(request.body)
    exercise_record_identifier = payload['exerciseRecord']
    weight = payload['weight']

    exercise_record = models.ExerciseRecord.objects.get(
        identifier=exercise_record_identifier,
        user=request.user,
    )

    exercise_record.planned_weight = int(weight)
    exercise_record.save()

    exercise_record.set_records.all().delete()

    _generate_set_records(exercise_record)

    return JsonResponse({
        'success': True,
        'exerciseRecord': _serialize_exercise_record(exercise_record),
    })

@transaction.atomic
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
            planned_weight=_get_planned_weight_for_user(program_exercise, request.user),
        )
        exercise_record.save()

        _generate_set_records(exercise_record, program_exercise)

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

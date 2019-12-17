from django.db import migrations

def create_data(apps, schema_editor):
    Program = apps.get_model('program', 'Program')
    ProgramWorkout = apps.get_model('program', 'ProgramWorkout')
    Exercise = apps.get_model('exercise', 'Exercise')

    program = Program(name='Basic Program')
    program.save()

    workout = ProgramWorkout(program=program, name='Workout A')
    workout.save()

    exercise = Exercise(
        name='Low bar squat',
    )
    exercise.save()
    workout.exercises.add(
        exercise,
        through_defaults={
            'weight': 45,
            'sets': 5,
            'reps': 5,
        },
    )

    exercise = Exercise(
        name='Bench press',
    )
    exercise.save()
    workout.exercises.add(
        exercise,
        through_defaults={
            'weight': 45,
            'sets': 5,
            'reps': 5,
        },
    )

    exercise = Exercise(
        name='Power clean',
    )
    exercise.save()
    workout.exercises.add(
        exercise,
        through_defaults={
            'weight': 45,
            'sets': 5,
            'reps': 3,
        },
    )

    workout = ProgramWorkout(program=program, name='Workout B')
    workout.save()

    exercise = Exercise(
        name='Front squat',
    )
    exercise.save()
    workout.exercises.add(
        exercise,
        through_defaults={
            'weight': 45,
            'sets': 5,
            'reps': 5,
        },
    )

    exercise = Exercise(
        name='Skullcrusher',
    )
    exercise.save()
    workout.exercises.add(
        exercise,
        through_defaults={
            'weight': 45,
            'sets': 5,
            'reps': 5,
        },
    )

    exercise = Exercise(
        name='Pendlay row',
    )
    exercise.save()
    workout.exercises.add(
        exercise,
        through_defaults={
            'weight': 45,
            'sets': 5,
            'reps': 5,
        },
    )

    workout = ProgramWorkout(program=program, name='Workout C')
    workout.save()

    exercise = Exercise(
        name='Deadlift',
    )
    exercise.save()
    workout.exercises.add(
        exercise,
        through_defaults={
            'weight': 45,
            'sets': 1,
            'reps': 5,
        },
    )

    exercise = Exercise(
        name='Overhead press',
    )
    exercise.save()
    workout.exercises.add(
        exercise,
        through_defaults={
            'weight': 45,
            'sets': 5,
            'reps': 5,
        },
    )

    exercise = Exercise(
        name='Pull up',
    )
    exercise.save()
    workout.exercises.add(
        exercise,
        through_defaults={
            'weight': 45,
            'sets': 5,
            'reps': 5,
        },
    )

class Migration(migrations.Migration):

    dependencies = [
        ('program', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_data),
    ]

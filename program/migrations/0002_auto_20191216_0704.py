from django.db import migrations

def create_data(apps, schema_editor):
    Program = apps.get_model('program', 'Program')
    Workout = apps.get_model('program', 'Workout')
    Exercise = apps.get_model('program', 'Exercise')

    program = Program(name='Basic Program')
    program.save()

    workout = Workout(program=program, name='Workout A')
    workout.save()

    exercise = Exercise(
        workout=workout,
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
        workout=workout,
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
        workout=workout,
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

    workout = Workout(program=program, name='Workout B')
    workout.save()

    exercise = Exercise(
        workout=workout,
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
        workout=workout,
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
        workout=workout,
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

    workout = Workout(program=program, name='Workout C')
    workout.save()

    exercise = Exercise(
        workout=workout,
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
        workout=workout,
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
        workout=workout,
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

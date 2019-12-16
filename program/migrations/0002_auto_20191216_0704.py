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
        weight=45,
        sets=5,
        reps=5,
    )
    exercise.save()

    exercise = Exercise(
        workout=workout,
        name='Bench press',
        weight=45,
        sets=5,
        reps=5,
    )
    exercise.save()

    exercise = Exercise(
        workout=workout,
        name='Power clean',
        weight=45,
        sets=5,
        reps=3,
    )
    exercise.save()

    workout = Workout(program=program, name='Workout B')
    workout.save()

    exercise = Exercise(
        workout=workout,
        name='Front squat',
        weight=45,
        sets=5,
        reps=5,
    )
    exercise.save()

    exercise = Exercise(
        workout=workout,
        name='Skullcrusher',
        weight=45,
        sets=5,
        reps=5,
    )
    exercise.save()

    exercise = Exercise(
        workout=workout,
        name='Pendlay row',
        weight=45,
        sets=5,
        reps=5,
    )
    exercise.save()

    workout = Workout(program=program, name='Workout C')
    workout.save()

    exercise = Exercise(
        workout=workout,
        name='Deadlift',
        weight=45,
        sets=1,
        reps=5,
    )
    exercise.save()

    exercise = Exercise(
        workout=workout,
        name='Overhead press',
        weight=45,
        sets=5,
        reps=5,
    )
    exercise.save()

    exercise = Exercise(
        workout=workout,
        name='Pull up',
        weight=45,
        sets=5,
        reps=5,
    )
    exercise.save()

class Migration(migrations.Migration):

    dependencies = [
        ('program', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_data),
    ]

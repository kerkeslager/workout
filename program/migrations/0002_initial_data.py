from django.db import migrations

def create_data(apps, schema_editor):
    Program = apps.get_model('program', 'Program')
    ProgramWorkout = apps.get_model('program', 'ProgramWorkout')
    ProgramExercise = apps.get_model('program', 'ProgramExercise')
    Exercise = apps.get_model('exercise', 'Exercise')

    program = Program(name='Basic Program')
    program.save()

    workout = ProgramWorkout(program=program, name='Workout A')
    workout.save()

    exercise = Exercise(
        name='Low bar squat',
    )
    exercise.save()
    program_exercise = ProgramExercise(
        workout=workout,
        exercise=exercise,
        start_weight=45,
        sets=5,
        reps=5,
        progression='LINR',
        progression_linear_increment=5,
    )
    program_exercise.save()

    exercise = Exercise(
        name='Bench press',
    )
    exercise.save()
    program_exercise = ProgramExercise(
        workout=workout,
        exercise=exercise,
        start_weight=45,
        sets=5,
        reps=5,
        progression='LINR',
        progression_linear_increment=5,
    )
    program_exercise.save()

    exercise = Exercise(
        name='Power clean',
    )
    exercise.save()
    program_exercise = ProgramExercise(
        workout=workout,
        exercise=exercise,
        start_weight=45,
        sets=5,
        reps=3,
        progression='LINR',
        progression_linear_increment=5,
    )
    program_exercise.save()

    workout = ProgramWorkout(program=program, name='Workout B')
    workout.save()

    exercise = Exercise(
        name='Front squat',
    )
    exercise.save()
    program_exercise = ProgramExercise(
        workout=workout,
        exercise=exercise,
        start_weight=45,
        sets=5,
        reps=5,
        progression='LINR',
        progression_linear_increment=5,
    )
    program_exercise.save()

    exercise = Exercise(
        name='Skullcrusher',
    )
    exercise.save()
    program_exercise = ProgramExercise(
        workout=workout,
        exercise=exercise,
        start_weight=25,
        sets=5,
        reps=5,
        progression='LINR',
        progression_linear_increment=5,
    )
    program_exercise.save()

    exercise = Exercise(
        name='Pendlay row',
    )
    exercise.save()
    program_exercise = ProgramExercise(
        workout=workout,
        exercise=exercise,
        start_weight=65,
        sets=5,
        reps=5,
        progression='LINR',
        progression_linear_increment=5,
    )
    program_exercise.save()

    workout = ProgramWorkout(program=program, name='Workout C')
    workout.save()

    exercise = Exercise(
        name='Deadlift',
    )
    exercise.save()
    program_exercise = ProgramExercise(
        workout=workout,
        exercise=exercise,
        start_weight=95,
        sets=1,
        reps=5,
        progression='LINR',
        progression_linear_increment=10,
    )
    program_exercise.save()

    exercise = Exercise(
        name='Overhead press',
    )
    exercise.save()
    program_exercise = ProgramExercise(
        workout=workout,
        exercise=exercise,
        start_weight=45,
        sets=5,
        reps=5,
        progression='LINR',
        progression_linear_increment=5,
    )
    program_exercise.save()

    exercise = Exercise(
        name='Pull up',
    )
    exercise.save()
    program_exercise = ProgramExercise(
        workout=workout,
        exercise=exercise,
        start_weight=45,
        sets=5,
        reps=5,
        progression='LINR',
        progression_linear_increment=5,
    )
    program_exercise.save()

class Migration(migrations.Migration):

    dependencies = [
        ('program', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_data),
    ]

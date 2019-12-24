# Generated by Django 3.0 on 2019-12-23 23:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('program', '0002_initial_data'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exercise', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('planned_weight', models.IntegerField()),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='exercise_records', to='exercise.Exercise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercise_records', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('program_workout', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='program.ProgramWorkout')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workout_records', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('programs', models.ManyToManyField(to='program.Program')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SetRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('planned_reps', models.IntegerField()),
                ('completed_reps', models.IntegerField(default=None, null=True)),
                ('weight', models.IntegerField()),
                ('is_work_set', models.BooleanField()),
                ('exercise_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='set_records', to='user.ExerciseRecord')),
            ],
        ),
        migrations.AddField(
            model_name='exerciserecord',
            name='workout_record',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercise_records', to='user.WorkoutRecord'),
        ),
    ]

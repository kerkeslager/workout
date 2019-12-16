import uuid

from django.db import models

class Program(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)

class Workout(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    program = models.ForeignKey(Program, models.CASCADE)
    name = models.CharField(max_length=256)
    exercises = models.ManyToManyField('Exercise', through='WorkoutExercise')

class Exercise(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, models.CASCADE)
    exercise = models.ForeignKey(Exercise, models.CASCADE)
    weight = models.IntegerField()
    sets = models.IntegerField()
    reps = models.IntegerField()

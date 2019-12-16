import uuid

from django.db import models

class Program(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Workout(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    program = models.ForeignKey(Program, models.CASCADE)
    name = models.CharField(max_length=256)
    exercises = models.ManyToManyField('Exercise', through='WorkoutExercise')

    def __str__(self):
        return self.name

class Exercise(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, models.CASCADE)
    exercise = models.ForeignKey(Exercise, models.CASCADE)
    weight = models.IntegerField()
    sets = models.IntegerField()
    reps = models.IntegerField()

    def __str__(self):
        return self.exercise.name

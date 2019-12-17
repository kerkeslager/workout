import uuid

from django.db import models

class Program(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class ProgramWorkout(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    program = models.ForeignKey('Program', models.CASCADE, related_name='workouts')
    name = models.CharField(max_length=256)
    exercises = models.ManyToManyField('exercise.Exercise', through='ProgramExercise')

    def __str__(self):
        return self.name

class ProgramExercise(models.Model):
    workout = models.ForeignKey('ProgramWorkout', models.CASCADE)
    exercise = models.ForeignKey('exercise.Exercise', models.CASCADE)
    weight = models.IntegerField()
    sets = models.IntegerField()
    reps = models.IntegerField()

    def __str__(self):
        return self.exercise.name

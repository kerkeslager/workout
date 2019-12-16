import uuid

from django.db import models

class Program(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)

class Workout(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    program = models.ForeignKey(Program, models.CASCADE)
    name = models.CharField(max_length=256)

class Exercise(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    workout = models.ForeignKey(Workout, models.CASCADE)
    name = models.CharField(max_length=256)
    weight = models.IntegerField()
    sets = models.IntegerField()
    reps = models.IntegerField()

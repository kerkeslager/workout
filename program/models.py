import uuid

from django.db import models

class Program(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return self.name

    def least_recent_program_workouts_for_user(self, user):
        program_workouts_and_most_recent_records = [
            (program_workout, program_workout.most_recent_record_for_user(user))
            for program_workout in self.workouts.all()
        ]

        never_done = [
            pw
            for pw, most_recent_record in program_workouts_and_most_recent_records
            if most_recent_record is None
        ]

        if any(never_done):
            return never_done

        return [next(sorted(pair, key=lambda pair: pair[1].created))[0]]

class ProgramWorkout(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    program = models.ForeignKey('Program', models.CASCADE, related_name='workouts')
    name = models.CharField(max_length=256, null=False, blank=False)
    exercises = models.ManyToManyField('exercise.Exercise', through='ProgramExercise')

    def __str__(self):
        return self.name

    def ongoing_for_user(self, user):
        from user import models as user_models
        return user_models.WorkoutRecord.objects.filter(
            user=user,
            program_workout=self,
            is_finished=False,
        ).first() is not None

    def most_recent_record_for_user(self, user):
        from user import models as user_models
        return user_models.WorkoutRecord.objects.filter(
            user=user,
            program_workout=self,
            is_finished=True,
        ).order_by('-created').first()

class ProgramExercise(models.Model):
    workout = models.ForeignKey('ProgramWorkout', models.CASCADE)
    exercise = models.ForeignKey('exercise.Exercise', models.CASCADE)
    weight = models.IntegerField(null=False)
    sets = models.IntegerField(null=False)
    reps = models.IntegerField(null=False)

    def __str__(self):
        return self.exercise.name

import uuid

from django.db import models

class Program(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return self.name

    def least_recent_program_workouts_for_user(self, user):
        never_done = []
        dates_to_program_workouts = {}

        for program_workout in self.workouts.all():
            most_recent_record = program_workout.most_recent_record_for_user(user)

            if most_recent_record:
                dates_to_program_workouts[most_recent_record.created] = program_workout

            else:
                never_done.append(program_workout)

        if any(never_done):
            return never_done

        least_recent_program_workout = dates_to_program_workouts[min(dates_to_program_workouts.keys())]

        return [least_recent_program_workout]

class ProgramWorkout(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    program = models.ForeignKey('Program', models.CASCADE, related_name='workouts')
    name = models.CharField(max_length=256, null=False, blank=False)

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
    workout = models.ForeignKey('ProgramWorkout', models.CASCADE, related_name='program_exercises')
    exercise = models.ForeignKey('exercise.Exercise', models.CASCADE)
    weight = models.IntegerField(null=False)
    sets = models.IntegerField(null=False)
    reps = models.IntegerField(null=False)

    def __str__(self):
        return self.exercise.name

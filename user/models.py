import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from exercise import models as exercise_models
from program import models as program_models

class UserProfile(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    programs = models.ManyToManyField('program.Program')

    @property
    def exercises(self):
        return exercise_models.Exercise.objects.filter(
            exercise_records__user=self.user,
            exercise_records__set_records__completed_reps__gt=0,
        )

    def get_recommended_program_workouts(self):
        ongoing = []
        least_recent_in_program = []

        for program in self.user.profile.programs.all():
            for program_workout in program.workouts.all():
                if program_workout.ongoing_for_user(self.user):
                    ongoing.append(program_workout)

            for program_workout in program.least_recent_program_workouts_for_user(self.user):
                least_recent_in_program.append(program_workout)

        if any(ongoing):
            return ongoing

        return least_recent_in_program

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        basic_program = program_models.Program.objects.all().first()

        profile = UserProfile.objects.create(user=instance)
        profile.programs.add(basic_program)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class WorkoutRecord(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_records')
    is_finished = models.BooleanField(null=False, default=False)
    program_workout = models.ForeignKey('program.ProgramWorkout', on_delete=models.PROTECT)

class ExerciseRecord(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercise_records')
    workout_record = models.ForeignKey(WorkoutRecord, on_delete=models.CASCADE, related_name='exercise_records')
    exercise = models.ForeignKey('exercise.Exercise', on_delete=models.PROTECT, related_name='exercise_records')
    planned_weight = models.IntegerField(null=False)

class SetRecord(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    exercise_record = models.ForeignKey(ExerciseRecord, on_delete=models.CASCADE, related_name='set_records')
    planned_reps = models.IntegerField(null=False)
    completed_reps = models.IntegerField(null=True, default=None)

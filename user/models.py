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
            exercise_records__set_records__reps_completed__gt=0,
        ).distinct()

    def get_recommended_program_workouts(self):
        ongoing = []
        least_recent_in_program = []

        for program in self.user.profile.programs.all():
            for program_workout in program.workouts.all():
                if program_workout.ongoing_for_user(self.user):
                    ongoing.append(program_workout)

            least_recent_in_program.append(
                program.least_recent_program_workout_for_user(self.user)
            )

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

    @property
    def succeeded(self):
        return all(set_record.succeeded for set_record in self.work_set_records.all())

    @property
    def warmup_set_records(self):
        return self.set_records.filter(warmup_or_work=SetRecord.WARMUP)

    @property
    def work_set_records(self):
        return self.set_records.filter(warmup_or_work=SetRecord.WORK)

class SetRecord(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    exercise_record = models.ForeignKey(ExerciseRecord, on_delete=models.CASCADE, related_name='set_records')
    weight = models.IntegerField()

    WARMUP = 'warmup'
    WORK = 'work'
    WARMUP_OR_WORK_CHOICES = (
        (WARMUP, 'Warmup'),
        (WORK, 'Work'),
    )
    warmup_or_work = models.CharField(max_length=6, choices=WARMUP_OR_WORK_CHOICES)

    REPS = 'reps'
    TIME = 'time'
    SUCCESS_CONDITION_CHOICES = (
        (REPS, 'Reps'),
        (TIME, 'Time'),
    )
    success_condition = models.CharField(max_length=4, choices=SUCCESS_CONDITION_CHOICES)

    reps_planned = models.IntegerField()
    reps_completed = models.IntegerField(null=True, default=None)

    @property
    def succeeded(self):
        return self.reps_planned == self.reps_completed

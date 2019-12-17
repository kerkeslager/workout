from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    programs = models.ManyToManyField('program.Program')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class WorkoutRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_records')
    complete = models.BooleanField(null=False, default=False)

class ExerciseRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercise_records')
    workout_record = models.ForeignKey(WorkoutRecord, on_delete=models.CASCADE)
    exercise = models.ForeignKey('exercise.Exercise', on_delete=models.PROTECT)

class SetRecord(models.Model):
    exercise_record = models.ForeignKey(ExerciseRecord, on_delete=models.CASCADE, related_name='set_records')
    planned_reps = models.IntegerField(null=False)
    completed_reps = models.IntegerField(null=True, default=None)

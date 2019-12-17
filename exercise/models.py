import uuid

from django.db import models

class Exercise(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    def most_recent_exercise_record_for_user(self, user):
        return self.exercise_records.filter(user=user).order_by('-created').first()

    def personal_best_record_for_user(self, user):
        return self.exercise_records.filter(user=user).order_by('-planned_weight').first()

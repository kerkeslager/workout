import uuid

from django.db import models

class Exercise(models.Model):
    BARBELL = 'BB'
    BODY_WEIGHT = 'BW'
    CURL_BAR = 'CB'
    DUMBBELL = 'DB'

    RESISTANCE_CHOICES = (
        (BARBELL, 'Barbell'),
        (BODY_WEIGHT, 'Body weight'),
        (CURL_BAR, 'Curl bar'),
        (DUMBBELL, 'Dumbbell'),
    )

    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    resistance = models.CharField(max_length=2, choices=RESISTANCE_CHOICES)

    def __str__(self):
        return self.name

    def most_recent_exercise_record_for_user(self, user):
        return self.exercise_records.filter(user=user).order_by('-created').first()

    def personal_best_record_for_user(self, user):
        return self.exercise_records.filter(user=user).order_by('-planned_weight').first()

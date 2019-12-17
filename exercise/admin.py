from django.contrib import admin

from . import models

class ExerciseAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Exercise, ExerciseAdmin)

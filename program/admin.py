from django.contrib import admin

from . import models

class ProgramExerciseInline(admin.TabularInline):
    model = models.ProgramExercise
    extra = 0

class ProgramWorkoutAdmin(admin.ModelAdmin):
    inlines = [ProgramExerciseInline]
admin.site.register(models.ProgramWorkout, ProgramWorkoutAdmin)

class ProgramAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Program, ProgramAdmin)

from django.contrib import admin

from . import models

class WorkoutExerciseInline(admin.TabularInline):
    model = models.WorkoutExercise
    extra = 0

class WorkoutAdmin(admin.ModelAdmin):
    inlines = [WorkoutExerciseInline]
admin.site.register(models.Workout, WorkoutAdmin)

class ProgramAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Program, ProgramAdmin)

class ExerciseAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Exercise, ExerciseAdmin)

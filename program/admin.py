from django.contrib import admin

from . import models

class ProgramAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Program, ProgramAdmin)

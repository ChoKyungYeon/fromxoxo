from django.contrib import admin

from letterapp.models import Letter


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ('writer', 'saver','created_at')
    ordering = ('-created_at',)
from accountapp.models import CustomUser
from django.contrib import admin

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phonenumber','created_at')
    ordering = ('-created_at',)

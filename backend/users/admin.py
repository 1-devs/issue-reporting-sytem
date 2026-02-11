from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'role', 'phone_number', 'assigned_location_id')
    list_filter = ('role',)
    search_fields = ('email', 'full_name', 'phone_number')
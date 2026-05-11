from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'organization')
    list_filter = ('role',)
    autocomplete_fields = ('user', 'organization')

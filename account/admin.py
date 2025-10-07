from django.contrib import admin
from .models import UserProfile

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_cuisine')
    list_filter = ('preferred_cuisine',)
    search_fields = ('user__username', 'preferred_cuisine')

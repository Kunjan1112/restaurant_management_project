from django.contrib import admin
from .models import Special

# Register your models here.


@admin.register(Special):
class SpecialAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'price', 'created_at')
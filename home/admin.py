from django.contrib import admin

from .models import Table, DailyOperatingHours

# Register the Table model

admin.site.register(Table)

admin.site.register(DailyOperatingHours)


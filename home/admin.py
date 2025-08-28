from django.contrib import admin
from .models import Special, Chef

# Register your models here.


@admin.register(Special)
class SpecialAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'price', 'created_at')

@admin.register(OpeningHour)
class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ("day","open_time", "close_time")

admin.site.register(Chef)

admin.site.register(RestaurantInfo)
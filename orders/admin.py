from django.contrib import admin
from .models import Order

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'created_at')
    list_filter = ('created_at',)
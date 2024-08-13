from django.contrib import admin
from .models import  Ad


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'start_date', 'end_date', 'is_active', 'clicks', 'impressions')
    list_filter = ('position', 'is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')
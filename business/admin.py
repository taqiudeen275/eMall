# admin.py
from django.contrib import admin
from .models import Business

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'category', 'city', 'country', 'phone', 'website')
    list_filter = ('category', 'country', 'state', 'city', 'size')
    search_fields = ('business_name', 'user__username', 'description', 'phone', 'website')
    readonly_fields = ('user',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'business_name', 'description', 'category', 'size')
        }),
        ('Contact Information', {
            'fields': ('phone', 'website', 'email')
        }),
        ('Location', {
            'fields': ('address', 'city', 'state', 'country', 'zip_code')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url')
        }),
        ('Additional Details', {
            'fields': ('logo', 'founded_date', 'operating_hours', 'tax_id')
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        return request.user.is_superuser or obj.user == request.user

    def has_delete_permission(self, request, obj=None):
        if not obj:
            return True
        return request.user.is_superuser or obj.user == request.user
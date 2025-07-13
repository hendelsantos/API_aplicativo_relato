from django.contrib import admin
from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'location_type', 'parent', 'level', 'is_active')
    list_filter = ('location_type', 'is_active')
    search_fields = ('code', 'name', 'description')
    ordering = ('parent', 'name')
    
    def level(self, obj):
        return obj.level
    level.short_description = 'Nível'

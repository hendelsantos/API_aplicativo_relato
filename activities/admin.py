from django.contrib import admin
from .models import (
    ActivityType, StandardQuestion, MaintenanceActivity,
    PartUsage, ActivityPhoto, ActivityAnswer
)


class StandardQuestionInline(admin.TabularInline):
    model = StandardQuestion
    extra = 1


@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'requires_parts', 'estimated_time', 'is_active')
    list_filter = ('requires_parts', 'is_active')
    search_fields = ('name', 'description')
    inlines = [StandardQuestionInline]


class PartUsageInline(admin.TabularInline):
    model = PartUsage
    extra = 0


class ActivityPhotoInline(admin.TabularInline):
    model = ActivityPhoto
    extra = 0


class ActivityAnswerInline(admin.TabularInline):
    model = ActivityAnswer
    extra = 0


@admin.register(MaintenanceActivity)
class MaintenanceActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'technician', 'activity_type', 'location', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority', 'activity_type', 'created_at')
    search_fields = ('title', 'description', 'technician__username', 'location__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PartUsageInline, ActivityPhotoInline, ActivityAnswerInline]

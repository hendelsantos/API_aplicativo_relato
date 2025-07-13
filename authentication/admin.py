from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'employee_id', 'shift', 'is_supervisor', 'is_active')
    list_filter = ('shift', 'is_supervisor', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'employee_id')
    ordering = ('username',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informações do Técnico', {
            'fields': ('employee_id', 'shift', 'phone', 'is_supervisor')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informações do Técnico', {
            'fields': ('employee_id', 'shift', 'phone', 'is_supervisor')
        }),
    )

from django.contrib import admin
from .models import Role, Organization

# Register your models here.


class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'create_date', 'create_by', 'modify_date', 'modify_by')


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'email', 'phone', 'is_active', 'create_by', 'modify_date', 'modify_by')


admin.site.register(Role, RoleAdmin)
admin.site.register(Organization, OrganizationAdmin)

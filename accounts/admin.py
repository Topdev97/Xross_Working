from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

from .models import *


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("email", "first_name", "last_name", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email","username", "first_name", "last_name", "password1", "password2", "avatar"),
            },
        ),
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


admin.site.register(User, UserAdmin)


class EmailAdmin(admin.ModelAdmin):
    """
    Admin part for managing the the Email model
    """
    list_display = ['to', 'subject', 'ok',]
    list_filter = ['ok']
    readonly_fields = ['when', 'to', 'subject', 'body', 'ok']
    search_fields = ['subject', 'body', 'to']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(Email, EmailAdmin)
admin.site.register(Employee)
admin.site.register(Employer)

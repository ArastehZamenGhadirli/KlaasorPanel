from django.contrib import admin
from accounts.models import CustomUser, CustomUserManager, BaseUserAdmin

# Register your models here.


class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = (
        "phone_number",
        "full_name",
        "is_staff",
        "is_support",
        "is_superuser",
        "is_active",
    )
    list_filter = ("is_staff", "is_superuser", "is_support", "is_active", "gender")
    search_fields = ("phone_number", "national_id")
    ordering = ("phone_number",)

    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("اطلاعات شخصی", {"fields": ("full_name", "national_id", "gender")}),
        (
            "دسترسی‌ها",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_support",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("تاریخ‌ها", {"fields": ("last_login",)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)

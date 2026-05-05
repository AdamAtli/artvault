from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.register(UserProfile)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"

class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

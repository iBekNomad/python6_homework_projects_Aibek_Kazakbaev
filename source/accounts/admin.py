from django.contrib import admin
from .models import AuthToken, Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

admin.site.register(AuthToken)


class ProfileInLine(admin.StackedInline):
    model = Profile
    exclude = []


class ProfileAdmin(UserAdmin):
    inlines = [ProfileInLine]


User = get_user_model()
admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)

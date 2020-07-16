from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile

class profile_inline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Users'

class user_admin(BaseUserAdmin):
    inlines = (profile_inline,)

admin.site.unregister(User)
admin.site.register(User,user_admin)

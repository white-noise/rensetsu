from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Kanji, UserProfile

# Show kanji individually
admin.site.register(Kanji)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Un-register and re-register inline views
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
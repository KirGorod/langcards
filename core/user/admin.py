from django.contrib import admin
from user.models import User


class UserAdmin(admin.ModelAdmin):
    model = User


admin.site.register(User)

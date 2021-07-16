from django.contrib import admin
from .models import userprofile

@admin.register(userprofile)

class adminuser(admin.ModelAdmin):
    list_display = ['user', 'reset_pass_token', 'email_verify', 'is_verified']
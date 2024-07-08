from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SafariUser, Event

# Register your models here.
admin.site.register(SafariUser, UserAdmin)
admin.site.register(Event)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import HealthUserCreationForm, HealthUserChangeForm
from .models import HealthUser

class HealthUserAdmin(UserAdmin):
    add_form = HealthUserCreationForm
    form = HealthUserChangeForm
    model = HealthUser
    list_display = ["email", "username",]

admin.site.register(HealthUser, HealthUserAdmin)
from django.contrib import admin
from .models import PersonalProfile

# Register your models here.

@admin.register(PersonalProfile)
class UserAdmin(admin.ModelAdmin):
    pass

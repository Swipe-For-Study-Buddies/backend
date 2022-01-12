from django.contrib import admin
from .models import PersonalProfile, Learn, Hobby, Skill

# Register your models here.

@admin.register(PersonalProfile)
class UserAdmin(admin.ModelAdmin):
    pass
@admin.register(Learn)
class LearnAdmin(admin.ModelAdmin):
    pass

@admin.register(Hobby)
class SkillAdmin(admin.ModelAdmin):
    pass

@admin.register(Skill)
class HobbyAdmin(admin.ModelAdmin):
    pass
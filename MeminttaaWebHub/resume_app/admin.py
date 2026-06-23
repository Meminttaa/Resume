from django.contrib import admin
from .models import UserProfile, Skill, AIMultinomialLog

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'github_url')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'level')
    list_filter = ('category',)

@admin.register(AIMultinomialLog)
class AIMultinomialLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'predicted_category', 'created_at')
    readonly_fields = ('created_at',)
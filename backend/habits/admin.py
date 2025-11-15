from django.contrib import admin
from .models import Habit, HabitSprint

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'validation_type', 'difficulty_level', 'is_active', 'created_at']
    list_filter = ['validation_type', 'difficulty_level', 'is_active', 'ai_generated']
    search_fields = ['title', 'user__email']

@admin.register(HabitSprint)
class HabitSprintAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'start_date', 'end_date', 'is_active', 'is_completed']
    list_filter = ['is_active', 'is_completed']
    search_fields = ['title', 'user__email']
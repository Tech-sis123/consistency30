from django.contrib import admin
from .models import Goal, Habit, DailyCheckIn, Streak, ProgressInsight, Milestone, UserStats

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'project_type', 'is_active', 'current_streak', 'created_at')
    list_filter = ('category', 'project_type', 'is_active', 'is_completed', 'created_at')
    search_fields = ('title', 'user__email', 'user__username')
    raw_id_fields = ('user',)
    date_hierarchy = 'created_at'

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('title', 'goal', 'validation_method', 'difficulty_level', 'is_active', 'current_streak', 'created_at')
    list_filter = ('validation_method', 'difficulty_level', 'is_active', 'created_at')
    search_fields = ('title', 'goal__title', 'goal__user__email')
    raw_id_fields = ('goal',)

@admin.register(DailyCheckIn)
class DailyCheckInAdmin(admin.ModelAdmin):
    list_display = ('habit', 'date', 'is_approved', 'ai_confidence', 'is_self_report', 'completed_at')
    list_filter = ('is_approved', 'is_self_report', 'date', 'created_at')
    search_fields = ('habit__title', 'habit__goal__user__email')
    raw_id_fields = ('habit',)
    date_hierarchy = 'date'

@admin.register(Streak)
class StreakAdmin(admin.ModelAdmin):
    list_display = ('user', 'habit', 'current_streak', 'longest_streak', 'last_checkin', 'updated_at')
    list_filter = ('last_checkin', 'updated_at')
    search_fields = ('user__email', 'habit__title')
    raw_id_fields = ('user', 'habit')

@admin.register(ProgressInsight)
class ProgressInsightAdmin(admin.ModelAdmin):
    list_display = ('user', 'insight_type', 'title', 'is_actionable', 'is_read', 'generated_at')
    list_filter = ('insight_type', 'is_actionable', 'is_read', 'is_applied', 'generated_at')
    search_fields = ('user__email', 'title', 'description')
    raw_id_fields = ('user', 'habit', 'goal')

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('user', 'milestone_type', 'title', 'target_value', 'current_value', 'is_achieved', 'created_at')
    list_filter = ('milestone_type', 'is_achieved', 'is_celebrated', 'created_at')
    search_fields = ('user__email', 'title', 'description')
    raw_id_fields = ('user', 'habit', 'goal')

@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_goals', 'completed_goals', 'current_streak', 'overall_success_rate', 'calculated_at')
    list_filter = ('calculated_at',)
    search_fields = ('user__email', 'user__username')
    raw_id_fields = ('user',)
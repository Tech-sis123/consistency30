from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile, AccountabilityPartner, UserSettings

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'onboarding_completed', 'created_at')
    list_filter = ('onboarding_completed', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Consistency30 Settings', {
            'fields': (
                'phone', 'timezone', 'preferred_checkin_time', 'onboarding_completed',
                'push_notifications', 'email_notifications', 'share_progress', 'trust_score'
            )
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Consistency30 Settings', {
            'fields': (
                'email', 'phone', 'timezone', 'preferred_checkin_time'
            )
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'primary_goal', 'daily_time_commitment', 'has_tried_before', 'created_at')
    list_filter = ('has_tried_before', 'created_at')
    search_fields = ('user__email', 'user__username', 'primary_goal')
    raw_id_fields = ('user',)

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'language', 'habit_reminders', 'created_at')
    list_filter = ('theme', 'language', 'habit_reminders')
    search_fields = ('user__email', 'user__username')
    raw_id_fields = ('user',)

@admin.register(AccountabilityPartner)
class AccountabilityPartnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'partner', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'partner__email')
    raw_id_fields = ('user', 'partner')
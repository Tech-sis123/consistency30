from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    preferred_checkin_time = models.TimeField(default='09:00')
    onboarding_completed = models.BooleanField(default=False)
    
    # Notification preferences
    push_notifications = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=False)
    
    # Privacy & social
    share_progress = models.BooleanField(default=False)
    trust_score = models.FloatField(default=1.0)  # For self-report reliability
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    groups = models.ManyToManyField(Group, related_name='user_related_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='user_related_permissions')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'users'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    primary_goal = models.TextField()
    motivation_why = models.TextField()
    daily_time_commitment = models.IntegerField(help_text='Minutes per day')
    has_tried_before = models.BooleanField(default=False)
    previous_attempts = models.TextField(blank=True)
    
    # Additional profile fields
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Preferences
    motivational_quotes = models.BooleanField(default=True)
    weekly_summaries = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - Profile"
    
    class Meta:
        db_table = 'user_profiles'

class AccountabilityPartner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partners')
    partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partner_of')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'partner']
        db_table = 'accountability_partners'

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    
    # Notification settings
    habit_reminders = models.BooleanField(default=True)
    streak_notifications = models.BooleanField(default=True)
    partner_activity = models.BooleanField(default=True)
    weekly_progress = models.BooleanField(default=True)
    
    # App preferences
    theme = models.CharField(max_length=20, default='light', choices=[
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto')
    ])
    language = models.CharField(max_length=10, default='en')
    
    # Privacy settings
    show_in_search = models.BooleanField(default=True)
    allow_partner_requests = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - Settings"
    
    class Meta:
        db_table = 'user_settings'
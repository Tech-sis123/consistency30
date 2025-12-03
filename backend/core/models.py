from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Goal(models.Model):
    GOAL_CATEGORIES = [
        ('fitness', 'Fitness'),
        ('learning', 'Learning'),
        ('productivity', 'Productivity'),
        ('health', 'Health'),
        ('creative', 'Creative'),
        ('mindfulness', 'Mindfulness'),
        ('other', 'Other'),
    ]
    
    PROJECT_TYPES = [
        ('30_day_challenge', '30-Day Challenge'),
        ('project_completion', 'Project Completion'),
        ('skill_development', 'Skill Development'),
        ('habit_formation', 'Habit Formation'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=GOAL_CATEGORIES)
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES, default='30_day_challenge')
    
    # 30-day project tracking
    project_title = models.CharField(max_length=200, blank=True)
    project_description = models.TextField(blank=True)
    start_date = models.DateField(default=timezone.now().date)
    target_end_date = models.DateField(null=True, blank=True)
    
    # Progress tracking
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    success_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    
    # Status
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'goals'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.target_end_date and self.project_type == '30_day_challenge':
            self.target_end_date = self.start_date + timezone.timedelta(days=30)
        super().save(*args, **kwargs)
    
    def calculate_success_rate(self):
        """Calculate success rate based on completed check-ins"""
        total_days = (timezone.now().date() - self.start_date).days + 1
        if total_days <= 0:
            return 0.0
        
        completed_checkins = self.habits.filter(
            checkins__date__gte=self.start_date,
            checkins__is_approved=True
        ).count()
        
        return min(completed_checkins / total_days, 1.0)

class Habit(models.Model):
    VALIDATION_METHODS = [
        ('photo', 'Photo'),
        ('audio', 'Audio'),
        ('text', 'Text'),
        ('screen_recording', 'Screen Recording'),
        ('self_report', 'Self Report'),
    ]
    
    DIFFICULTY_LEVELS = [
        (1, 'Very Easy'),
        (2, 'Easy'),
        (3, 'Moderate'),
        (4, 'Challenging'),
        (5, 'Very Challenging'),
    ]
    
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='habits')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    validation_method = models.CharField(max_length=20, choices=VALIDATION_METHODS)
    
    # Configuration
    target_duration = models.IntegerField(default=1, help_text="Minutes")  # For timed habits
    target_count = models.IntegerField(default=1, help_text="For countable habits")
    difficulty_level = models.IntegerField(choices=DIFFICULTY_LEVELS, default=3)
    preferred_time = models.TimeField(null=True, blank=True)
    
    # AI Validation
    validation_prompt = models.TextField(help_text="What the AI should look for")
    min_confidence = models.FloatField(default=0.85, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    
    # Progress tracking
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    total_completions = models.IntegerField(default=0)
    success_rate = models.FloatField(default=0.0)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'habits'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.goal.title} - {self.title}"
    
    def update_streak(self):
        """Update streak based on recent check-ins"""
        from django.utils import timezone
        from datetime import timedelta
        
        recent_checkins = self.checkins.filter(
            is_approved=True
        ).order_by('-date')[:7]  # Check last 7 days
        
        current_streak = 0
        check_date = timezone.now().date()
        
        for i in range(7):
            if any(checkin.date == check_date for checkin in recent_checkins):
                current_streak += 1
                check_date -= timedelta(days=1)
            else:
                break
        
        self.current_streak = current_streak
        self.longest_streak = max(self.longest_streak, current_streak)
        self.save()

class DailyCheckIn(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='checkins')
    date = models.DateField(default=timezone.now)
    
    # Validation data
    photo_proof = models.ImageField(upload_to='checkin_photos/', null=True, blank=True)
    audio_proof = models.FileField(upload_to='checkin_audio/', null=True, blank=True)
    text_proof = models.TextField(blank=True)
    screen_recording_proof = models.FileField(upload_to='screen_recordings/', null=True, blank=True)
    
    # AI Validation results
    ai_confidence = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    ai_feedback = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    validated_at = models.DateTimeField(null=True, blank=True)
    
    # Self-report fallback
    is_self_report = models.BooleanField(default=False)
    self_report_description = models.TextField(blank=True)
    
    # Timing and completion
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent = models.IntegerField(null=True, blank=True, help_text="Time spent in minutes")
    
    # User feedback
    difficulty_rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'daily_checkins'
        unique_together = ['habit', 'date']
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.habit.title} - {self.date}"
    
    def save(self, *args, **kwargs):
        if self.is_approved and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)
        
        # Update habit streak when check-in is approved
        if self.is_approved:
            self.habit.update_streak()

class Streak(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='streaks')
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='streaks')
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_checkin = models.DateField(null=True, blank=True)
    started_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'streaks'
        unique_together = ['user', 'habit']
    
    def __str__(self):
        return f"{self.user.email} - {self.habit.title} ({self.current_streak} days)"

class ProgressInsight(models.Model):
    INSIGHT_TYPES = [
        ('success_pattern', 'Success Pattern'),
        ('struggle_detection', 'Struggle Detection'),
        ('time_optimization', 'Time Optimization'),
        ('difficulty_adjustment', 'Difficulty Adjustment'),
        ('milestone_celebration', 'Milestone Celebration'),
        ('general_insight', 'General Insight'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='insights')
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='insights', null=True, blank=True)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='insights', null=True, blank=True)
    
    insight_type = models.CharField(max_length=30, choices=INSIGHT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    data = models.JSONField(default=dict)  # Flexible data storage
    
    # Actionability
    is_actionable = models.BooleanField(default=False)
    action_title = models.CharField(max_length=200, blank=True)
    action_description = models.TextField(blank=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    is_applied = models.BooleanField(default=False)
    
    # Timestamps
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'progress_insights'
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.insight_type}"

class Milestone(models.Model):
    MILESTONE_TYPES = [
        ('streak', 'Streak'),
        ('completion', 'Completion'),
        ('consistency', 'Consistency'),
        ('progress', 'Progress'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='milestones')
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='milestones', null=True, blank=True)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='milestones', null=True, blank=True)
    
    milestone_type = models.CharField(max_length=20, choices=MILESTONE_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_value = models.IntegerField()
    current_value = models.IntegerField()
    is_achieved = models.BooleanField(default=False)
    achieved_at = models.DateTimeField(null=True, blank=True)
    
    # Rewards or celebrations
    celebration_message = models.TextField(blank=True)
    is_celebrated = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'milestones'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"

class UserStats(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stats')
    
    # Overall stats
    total_goals = models.IntegerField(default=0)
    completed_goals = models.IntegerField(default=0)
    total_habits = models.IntegerField(default=0)
    active_habits = models.IntegerField(default=0)
    
    # Consistency stats
    overall_success_rate = models.FloatField(default=0.0)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    total_checkins = models.IntegerField(default=0)
    
    # Time-based stats
    total_time_invested = models.IntegerField(default=0, help_text="Total minutes invested")
    average_daily_time = models.FloatField(default=0.0)
    
    # Achievement stats
    milestones_achieved = models.IntegerField(default=0)
    insights_generated = models.IntegerField(default=0)
    
    # Timestamps
    calculated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_stats'
    
    def __str__(self):
        return f"{self.user.email} - Stats"
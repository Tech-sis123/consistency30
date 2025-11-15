from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Habit(models.Model):
    VALIDATION_TYPES = [
        ('photo', 'Photo'),
        ('audio', 'Audio'),
        ('text', 'Text'),
        ('screen_recording', 'Screen Recording'),
        ('self_report', 'Self Report'),
    ]
    
    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    title = models.CharField(max_length=200)
    description = models.TextField()
    validation_type = models.CharField(max_length=20, choices=VALIDATION_TYPES)
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, default='medium')
    target_duration = models.IntegerField(help_text='Target duration in minutes')
    is_active = models.BooleanField(default=True)
    ai_generated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"

class HabitSprint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sprints')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    habits = models.ManyToManyField(Habit, related_name='sprints')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Goal, Habit, DailyCheckIn, UserStats

@receiver(post_save, sender=Goal)
def update_user_stats_goal(sender, instance, created, **kwargs):
    """Update user stats when goals are created or updated"""
    if hasattr(instance.user, 'stats'):
        stats = instance.user.stats
        stats.total_goals = Goal.objects.filter(user=instance.user).count()
        stats.completed_goals = Goal.objects.filter(user=instance.user, is_completed=True).count()
        stats.save()

@receiver(post_save, sender=Habit)
@receiver(post_delete, sender=Habit)
def update_user_stats_habit(sender, instance, **kwargs):
    """Update user stats when habits are created, updated, or deleted"""
    if hasattr(instance.goal.user, 'stats'):
        stats = instance.goal.user.stats
        stats.total_habits = Habit.objects.filter(goal__user=instance.goal.user).count()
        stats.active_habits = Habit.objects.filter(goal__user=instance.goal.user, is_active=True).count()
        stats.save()

@receiver(post_save, sender=DailyCheckIn)
def update_streaks_on_checkin(sender, instance, created, **kwargs):
    """Update streaks when check-ins are approved"""
    if instance.is_approved and created:
        # Update habit streak
        instance.habit.update_streak()
        
        # Update user stats
        if hasattr(instance.habit.goal.user, 'stats'):
            stats = instance.habit.goal.user.stats
            stats.total_checkins = DailyCheckIn.objects.filter(
                habit__goal__user=instance.habit.goal.user,
                is_approved=True
            ).count()
            stats.save()
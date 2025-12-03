from celery import shared_task
from django.utils import timezone
from core.models import DailyCheckIn
from .models import ValidationLog
from .services import AIService

@shared_task
def validate_checkin_task(checkin_id):
    """Async task to validate a check-in"""
    try:
        checkin = DailyCheckIn.objects.get(id=checkin_id)
        ai_service = AIService()
        result = ai_service.validate_checkin(checkin)
        
        if result['success']:
            checkin.ai_confidence = result['confidence']
            checkin.ai_feedback = result['explanation']
            checkin.is_approved = result['is_approved']
            checkin.validated_at = timezone.now()
            checkin.save()
        
        return {
            'checkin_id': checkin_id,
            'success': result['success'],
            'is_approved': result.get('is_approved', False),
            'confidence': result.get('confidence', 0)
        }
        
    except DailyCheckIn.DoesNotExist:
        return {'error': 'Check-in not found', 'checkin_id': checkin_id}
    except Exception as e:
        return {'error': str(e), 'checkin_id': checkin_id}

@shared_task
def generate_weekly_insights_task():
    """Generate weekly insights for all active users"""
    from django.contrib.auth import get_user_model
    from core.models import ProgressInsight
    from .services import InsightGenerator
    
    User = get_user_model()
    insight_generator = InsightGenerator()
    
    active_users = User.objects.filter(
        is_active=True,
        goals__is_active=True
    ).distinct()
    
    insights_created = 0
    
    for user in active_users:
        try:
            insights_data = insight_generator.generate_weekly_insights(user)
            
            ProgressInsight.objects.create(
                user=user,
                insight_type='general_insight',
                title='Weekly Progress Insights',
                description=insights_data.get('suggestion', ''),
                data=insights_data,
                is_actionable=True,
                action_title=insights_data.get('suggestion', 'Weekly suggestion'),
                action_description=insights_data.get('improvement_area', '')
            )
            
            insights_created += 1
            
        except Exception as e:
            print(f"Failed to generate insights for user {user.email}: {str(e)}")
    
    return {'insights_created': insights_created, 'total_users': active_users.count()}

@shared_task
def cleanup_old_cache_entries():
    """Clean up old cache entries"""
    from .models import ValidationCache
    from django.utils import timezone
    from datetime import timedelta
    
    cutoff_date = timezone.now() - timedelta(days=30)
    deleted_count, _ = ValidationCache.objects.filter(
        last_used__lt=cutoff_date
    ).delete()
    
    return {'deleted_count': deleted_count}
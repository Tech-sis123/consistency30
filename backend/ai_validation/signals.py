from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ValidationLog, ModelPerformance
from django.utils import timezone

@receiver(post_save, sender=ValidationLog)
def update_model_performance(sender, instance, created, **kwargs):
    """Update model performance metrics when validation logs are created"""
    if created and instance.validation_rule:
        today = timezone.now().date()
        
        # Get or create performance record for today
        performance, created = ModelPerformance.objects.get_or_create(
            validation_rule=instance.validation_rule,
            date=today,
            defaults={
                'total_requests': 0,
                'successful_requests': 0,
                'failed_requests': 0,
                'average_confidence': 0,
                'average_processing_time': 0,
                'false_positives': 0,
                'false_negatives': 0,
            }
        )
        
        # Update metrics
        performance.total_requests += 1
        
        if instance.success:
            performance.successful_requests += 1
        else:
            performance.failed_requests += 1
        
        # Update average confidence (moving average)
        if instance.confidence_score:
            current_avg = performance.average_confidence
            total_successful = performance.successful_requests
            performance.average_confidence = (
                (current_avg * (total_successful - 1) + instance.confidence_score) / total_successful
                if total_successful > 0 else instance.confidence_score
            )
        
        # Update average processing time
        current_avg_time = performance.average_processing_time
        total_requests = performance.total_requests
        performance.average_processing_time = (
            (current_avg_time * (total_requests - 1) + instance.processing_time) / total_requests
        )
        
        performance.save()
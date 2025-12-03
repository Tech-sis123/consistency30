from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.utils import timezone
from .models import AIConfig, ValidationRule, ValidationLog, AITrainingData, AIFeedback, ModelPerformance
from .serializers import (
    ValidationRequestSerializer, ManualValidationSerializer, InsightGenerationSerializer,
    AIFeedbackSerializer, ValidationLogSerializer, ModelPerformanceSerializer
)
from .services import AIService, InsightGenerator
from core.models import DailyCheckIn, ProgressInsight

class ValidateCheckInView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ValidationRequestSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        checkin_id = serializer.validated_data['checkin_id']
        checkin = get_object_or_404(
            DailyCheckIn, 
            id=checkin_id,
            habit__goal__user=request.user
        )
        
        # Don't re-validate already approved check-ins
        if checkin.is_approved:
            return Response({
                'detail': 'Check-in already approved',
                'is_approved': True,
                'confidence': checkin.ai_confidence
            })
        
        # Perform AI validation
        ai_service = AIService()
        result = ai_service.validate_checkin(checkin)
        
        # Update check-in with results
        if result['success']:
            checkin.ai_confidence = result['confidence']
            checkin.ai_feedback = result['explanation']
            checkin.is_approved = result['is_approved']
            checkin.validated_at = timezone.now()
            checkin.save()
            
            # Create validation log
            validation_rule = ai_service._get_validation_rule(checkin)
            if validation_rule:
                ValidationLog.objects.create(
                    checkin=checkin,
                    validation_rule=validation_rule,
                    input_data_preview=ai_service._get_input_preview(checkin),
                    ai_response_raw=result.get('raw_response', ''),
                    ai_response_parsed=result.get('parsed_data', {}),
                    confidence_score=result['confidence'],
                    is_approved=result['is_approved'],
                    processing_time=result.get('processing_time', 0),
                    success=True,
                    completed_at=timezone.now()
                )
        
        return Response({
            'success': result['success'],
            'is_approved': result['is_approved'],
            'confidence': result['confidence'],
            'feedback': result['explanation'],
            'from_cache': result.get('from_cache', False),
            'error': result.get('error')
        })

class ManualValidationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ManualValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        checkin_id = serializer.validated_data['checkin_id']
        is_approved = serializer.validated_data['is_approved']
        admin_notes = serializer.validated_data.get('admin_notes', '')
        
        checkin = get_object_or_404(DailyCheckIn, id=checkin_id)
        
        # Update check-in
        checkin.is_approved = is_approved
        checkin.ai_confidence = 1.0 if is_approved else 0.0
        checkin.ai_feedback = f"Manually validated: {admin_notes}" if admin_notes else "Manually validated"
        checkin.validated_at = timezone.now()
        checkin.save()
        
        # Log the manual validation
        ValidationLog.objects.create(
            checkin=checkin,
            validation_rule=None,  # No AI rule for manual validation
            input_data_preview="Manual validation",
            ai_response_raw="",
            ai_response_parsed={"manual_validation": True},
            confidence_score=1.0,
            is_approved=is_approved,
            processing_time=0,
            success=True,
            completed_at=timezone.now()
        )
        
        return Response({
            'detail': 'Check-in manually validated',
            'is_approved': is_approved
        })

class GenerateInsightsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = InsightGenerationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        insight_generator = InsightGenerator()
        insights_data = insight_generator.generate_weekly_insights(request.user)
        
        # Save insights to database
        insight = ProgressInsight.objects.create(
            user=request.user,
            insight_type='general_insight',
            title='Weekly Progress Insights',
            description=insights_data.get('suggestion', ''),
            data=insights_data,
            is_actionable=True,
            action_title=insights_data.get('suggestion', 'Try this suggestion'),
            action_description=insights_data.get('improvement_area', '')
        )
        
        return Response({
            'insights': insights_data,
            'insight_id': insight.id,
            'generated_at': timezone.now()
        })

class AIFeedbackCreateView(generics.CreateAPIView):
    serializer_class = AIFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return AIFeedback.objects.filter(user=self.request.user)

class UserValidationLogsView(generics.ListAPIView):
    serializer_class = ValidationLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ValidationLog.objects.filter(
            checkin__habit__goal__user=self.request.user
        ).select_related('checkin', 'checkin__habit', 'validation_rule').order_by('-created_at')

class AIPerformanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Only show basic performance metrics to regular users
        today = timezone.now().date()
        
        user_validations = ValidationLog.objects.filter(
            checkin__habit__goal__user=request.user
        )
        
        total_validations = user_validations.count()
        successful_validations = user_validations.filter(success=True).count()
        average_confidence = user_validations.aggregate(avg_conf=Avg('confidence_score'))['avg_conf'] or 0
        
        today_validations = user_validations.filter(created_at__date=today)
        today_successful = today_validations.filter(success=True).count()
        
        return Response({
            'user_metrics': {
                'total_validations': total_validations,
                'success_rate': successful_validations / total_validations if total_validations > 0 else 0,
                'average_confidence': round(average_confidence, 2),
                'today_validations': today_validations.count(),
                'today_success_rate': today_successful / today_validations.count() if today_validations.count() > 0 else 0,
            }
        })

class ClearValidationCacheView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        from .models import ValidationCache
        from django.utils import timezone
        from datetime import timedelta
        
        # Clear cache entries older than 30 days
        cutoff_date = timezone.now() - timedelta(days=30)
        deleted_count, _ = ValidationCache.objects.filter(
            last_used__lt=cutoff_date
        ).delete()
        
        return Response({
            'detail': f'Cleared {deleted_count} old cache entries',
            'cleared_count': deleted_count
        })

class RetryFailedValidationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, log_id):
        validation_log = get_object_or_404(
            ValidationLog, 
            id=log_id,
            checkin__habit__goal__user=request.user,
            success=False
        )
        
        # Retry validation
        ai_service = AIService()
        result = ai_service.validate_checkin(validation_log.checkin)
        
        if result['success']:
            # Update validation log
            validation_log.retry_count += 1
            validation_log.success = True
            validation_log.confidence_score = result['confidence']
            validation_log.is_approved = result['is_approved']
            validation_log.ai_response_raw = result.get('raw_response', '')
            validation_log.ai_response_parsed = result.get('parsed_data', {})
            validation_log.processing_time = result.get('processing_time', 0)
            validation_log.completed_at = timezone.now()
            validation_log.save()
            
            # Update check-in
            checkin = validation_log.checkin
            checkin.ai_confidence = result['confidence']
            checkin.ai_feedback = result['explanation']
            checkin.is_approved = result['is_approved']
            checkin.validated_at = timezone.now()
            checkin.save()
        
        return Response({
            'success': result['success'],
            'is_approved': result.get('is_approved', False),
            'confidence': result.get('confidence', 0),
            'retry_count': validation_log.retry_count
        })
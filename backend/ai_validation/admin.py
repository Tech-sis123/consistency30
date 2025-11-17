from django.contrib import admin
from .models import AIConfig, ValidationRule, ValidationLog, AITrainingData, AIFeedback, ModelPerformance, ValidationCache

@admin.register(AIConfig)
class AIConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_name', 'is_active', 'created_at')
    list_filter = ('model_name', 'is_active', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Configuration', {
            'fields': ('name', 'api_key', 'model_name', 'is_active')
        }),
        ('Model Settings', {
            'fields': ('max_tokens', 'temperature')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ValidationRule)
class ValidationRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'validation_type', 'confidence_threshold', 'is_active', 'created_at')
    list_filter = ('validation_type', 'is_active', 'created_at')
    search_fields = ('name', 'prompt_template')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ValidationLog)
class ValidationLogAdmin(admin.ModelAdmin):
    list_display = ('checkin', 'validation_rule', 'success', 'is_approved', 'confidence_score', 'processing_time', 'created_at')
    list_filter = ('success', 'is_approved', 'validation_rule__validation_type', 'created_at')
    search_fields = ('checkin__habit__title', 'checkin__habit__goal__user__email')
    readonly_fields = ('created_at', 'completed_at')
    raw_id_fields = ('checkin', 'validation_rule')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('checkin', 'checkin__habit', 'validation_rule')

@admin.register(AITrainingData)
class AITrainingDataAdmin(admin.ModelAdmin):
    list_display = ('data_type', 'is_correct', 'confidence_score', 'used_for_training', 'created_at')
    list_filter = ('data_type', 'is_correct', 'used_for_training', 'created_at')
    search_fields = ('input_data', 'notes')
    readonly_fields = ('created_at',)

@admin.register(AIFeedback)
class AIFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback_type', 'checkin', 'is_resolved', 'created_at')
    list_filter = ('feedback_type', 'is_resolved', 'created_at')
    search_fields = ('user__email', 'description', 'expected_result')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('user', 'checkin')

@admin.register(ModelPerformance)
class ModelPerformanceAdmin(admin.ModelAdmin):
    list_display = ('validation_rule', 'date', 'total_requests', 'successful_requests', 'average_confidence', 'user_accuracy_score')
    list_filter = ('date', 'validation_rule__validation_type')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('validation_rule')

@admin.register(ValidationCache)
class ValidationCacheAdmin(admin.ModelAdmin):
    list_display = ('input_hash_short', 'validation_rule', 'is_approved', 'usage_count', 'last_used')
    list_filter = ('is_approved', 'last_used')
    search_fields = ('input_data_preview',)
    readonly_fields = ('created_at', 'last_used')
    
    def input_hash_short(self, obj):
        return obj.input_hash[:16] + '...'
    input_hash_short.short_description = 'Input Hash'
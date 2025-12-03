from rest_framework import serializers
from .models import AIConfig, ValidationRule, ValidationLog, AITrainingData, AIFeedback, ModelPerformance, ValidationCache

class AIConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIConfig
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class ValidationRuleSerializer(serializers.ModelSerializer):
    usage_count = serializers.SerializerMethodField()
    success_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = ValidationRule
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def get_usage_count(self, obj):
        return obj.validationlog_set.count()
    
    def get_success_rate(self, obj):
        success_count = obj.validationlog_set.filter(success=True).count()
        total_count = obj.validationlog_set.count()
        return success_count / total_count if total_count > 0 else 0

class ValidationLogSerializer(serializers.ModelSerializer):
    habit_title = serializers.CharField(source='checkin.habit.title', read_only=True)
    user_email = serializers.CharField(source='checkin.habit.goal.user.email', read_only=True)
    validation_rule_name = serializers.CharField(source='validation_rule.name', read_only=True)
    
    class Meta:
        model = ValidationLog
        fields = '__all__'
        read_only_fields = ('created_at', 'completed_at')

class AITrainingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AITrainingData
        fields = '__all__'
        read_only_fields = ('created_at',)

class AIFeedbackSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    habit_title = serializers.CharField(source='checkin.habit.title', read_only=True)

    class Meta:
        model = AIFeedback
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')  # Add 'user' to read_only_fields

    def validate_checkin(self, value):
        if value.habit.goal.user != self.context['request'].user:
            raise serializers.ValidationError("You can only create feedback for your own check-ins.")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ModelPerformanceSerializer(serializers.ModelSerializer):
    validation_rule_name = serializers.CharField(source='validation_rule.name', read_only=True)
    success_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = ModelPerformance
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def get_success_rate(self, obj):
        if obj.total_requests == 0:
            return 0.0
        return obj.successful_requests / obj.total_requests

class ValidationCacheSerializer(serializers.ModelSerializer):
    validation_rule_name = serializers.CharField(source='validation_rule.name', read_only=True)
    
    class Meta:
        model = ValidationCache
        fields = '__all__'
        read_only_fields = ('created_at', 'last_used')

class ValidationRequestSerializer(serializers.Serializer):
    checkin_id = serializers.IntegerField(required=True)
    
    def validate_checkin_id(self, value):
        from core.models import DailyCheckIn
        try:
            checkin = DailyCheckIn.objects.get(id=value)
            if checkin.habit.goal.user != self.context['request'].user:
                raise serializers.ValidationError("You can only validate your own check-ins.")
            return value
        except DailyCheckIn.DoesNotExist:
            raise serializers.ValidationError("Check-in not found.")

class ManualValidationSerializer(serializers.Serializer):
    checkin_id = serializers.IntegerField(required=True)
    is_approved = serializers.BooleanField(required=True)
    admin_notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_checkin_id(self, value):
        from core.models import DailyCheckIn
        try:
            checkin = DailyCheckIn.objects.get(id=value)
            return value
        except DailyCheckIn.DoesNotExist:
            raise serializers.ValidationError("Check-in not found.")

class InsightGenerationSerializer(serializers.Serializer):
    time_period = serializers.ChoiceField(
        choices=[('week', 'Last Week'), ('month', 'Last Month'), ('all', 'All Time')],
        default='week'
    )
    include_habits = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
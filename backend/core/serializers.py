from rest_framework import serializers
from .models import Goal, Habit, DailyCheckIn, Streak, ProgressInsight, Milestone, UserStats

class GoalSerializer(serializers.ModelSerializer):
    habit_count = serializers.SerializerMethodField()
    completed_habits_today = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()
    
    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at', 'current_streak', 'longest_streak', 'success_rate')
    
    def get_habit_count(self, obj):
        return obj.habits.count()
    
    def get_completed_habits_today(self, obj):
        from django.utils import timezone
        today = timezone.now().date()
        return obj.habits.filter(
            checkins__date=today,
            checkins__is_approved=True
        ).count()
    
    def get_progress_percentage(self, obj):
        return obj.calculate_success_rate()
    
    def get_days_remaining(self, obj):
        from django.utils import timezone
        if obj.target_end_date:
            remaining = (obj.target_end_date - timezone.now().date()).days
            return max(0, remaining)
        return None
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class HabitSerializer(serializers.ModelSerializer):
    goal_title = serializers.CharField(source='goal.title', read_only=True)
    today_checkin = serializers.SerializerMethodField()
    completion_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'current_streak', 'longest_streak', 'total_completions', 'success_rate')
    
    def get_today_checkin(self, obj):
        from django.utils import timezone
        today = timezone.now().date()
        try:
            checkin = obj.checkins.get(date=today)
            return {
                'id': checkin.id,
                'is_approved': checkin.is_approved,
                'completed_at': checkin.completed_at
            }
        except DailyCheckIn.DoesNotExist:
            return None
    
    def get_completion_rate(self, obj):
        total_checkins = obj.checkins.count()
        approved_checkins = obj.checkins.filter(is_approved=True).count()
        return approved_checkins / total_checkins if total_checkins > 0 else 0
    
    def validate(self, attrs):
        # Ensure the goal belongs to the current user
        if 'goal' in attrs and attrs['goal'].user != self.context['request'].user:
            raise serializers.ValidationError({"goal": "You can only create habits for your own goals."})
        return attrs

class DailyCheckInSerializer(serializers.ModelSerializer):
    habit_title = serializers.CharField(source='habit.title', read_only=True)
    goal_title = serializers.CharField(source='habit.goal.title', read_only=True)
    validation_method = serializers.CharField(source='habit.validation_method', read_only=True)
    
    class Meta:
        model = DailyCheckIn
        fields = '__all__'
        read_only_fields = ('ai_confidence', 'ai_feedback', 'is_approved', 'validated_at', 'created_at', 'updated_at')
    
    def validate(self, attrs):
        # Ensure the habit belongs to the current user
        if 'habit' in attrs and attrs['habit'].goal.user != self.context['request'].user:
            raise serializers.ValidationError({"habit": "You can only check in for your own habits."})
        
        # Validate proof based on validation method
        habit = attrs.get('habit')
        if habit:
            validation_method = habit.validation_method
            
            if validation_method == 'photo' and not attrs.get('photo_proof'):
                raise serializers.ValidationError({"photo_proof": "Photo proof is required for this habit."})
            
            elif validation_method == 'audio' and not attrs.get('audio_proof'):
                raise serializers.ValidationError({"audio_proof": "Audio proof is required for this habit."})
            
            elif validation_method == 'text' and not attrs.get('text_proof'):
                raise serializers.ValidationError({"text_proof": "Text proof is required for this habit."})
            
            elif validation_method == 'screen_recording' and not attrs.get('screen_recording_proof'):
                raise serializers.ValidationError({"screen_recording_proof": "Screen recording proof is required for this habit."})
            
            elif validation_method == 'self_report':
                attrs['is_self_report'] = True
                if not attrs.get('self_report_description'):
                    raise serializers.ValidationError({"self_report_description": "Description is required for self-report."})
        
        return attrs
    
    def create(self, validated_data):
        # Set date to today if not provided
        if 'date' not in validated_data:
            from django.utils import timezone
            validated_data['date'] = timezone.now().date()
        
        checkin = super().create(validated_data)
        
        # Trigger AI validation if not self-report
        if not checkin.is_self_report:
            from ai_validation.tasks import validate_checkin_task
            validate_checkin_task.delay(checkin.id)
        
        return checkin

class StreakSerializer(serializers.ModelSerializer):
    habit_title = serializers.CharField(source='habit.title', read_only=True)
    goal_title = serializers.CharField(source='habit.goal.title', read_only=True)
    
    class Meta:
        model = Streak
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

class ProgressInsightSerializer(serializers.ModelSerializer):
    habit_title = serializers.CharField(source='habit.title', read_only=True)
    goal_title = serializers.CharField(source='goal.title', read_only=True)
    
    class Meta:
        model = ProgressInsight
        fields = '__all__'
        read_only_fields = ('user', 'generated_at')

class MilestoneSerializer(serializers.ModelSerializer):
    habit_title = serializers.CharField(source='habit.title', read_only=True)
    goal_title = serializers.CharField(source='goal.title', read_only=True)
    
    class Meta:
        model = Milestone
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStats
        fields = '__all__'
        read_only_fields = ('user', 'calculated_at')

class GoalCreateSerializer(serializers.ModelSerializer):
    habits = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Goal
        fields = ('title', 'description', 'category', 'project_type', 
                 'project_title', 'project_description', 'start_date', 'habits')
    
    def create(self, validated_data):
        habits_data = validated_data.pop('habits', [])
        goal = Goal.objects.create(**validated_data)
        
        # Create associated habits
        for habit_data in habits_data:
            Habit.objects.create(goal=goal, **habit_data)
        
        return goal

class CheckInBulkSerializer(serializers.Serializer):
    habit_id = serializers.IntegerField()
    proof_data = serializers.DictField()
    
    def validate_habit_id(self, value):
        try:
            habit = Habit.objects.get(id=value)
            if habit.goal.user != self.context['request'].user:
                raise serializers.ValidationError("You can only check in for your own habits.")
            return value
        except Habit.DoesNotExist:
            raise serializers.ValidationError("Habit does not exist.")

class TodayCheckInsSerializer(serializers.Serializer):
    date = serializers.DateField()
    habits = HabitSerializer(many=True)
    completed_checkins = DailyCheckInSerializer(many=True)
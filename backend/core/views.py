from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.db.models import Q, Count, Avg
from django.shortcuts import get_object_or_404
from .models import Goal, Habit, DailyCheckIn, Streak, ProgressInsight, Milestone, UserStats
from .serializers import (
    GoalSerializer, HabitSerializer, DailyCheckInSerializer,
    StreakSerializer, ProgressInsightSerializer, MilestoneSerializer,
    UserStatsSerializer, GoalCreateSerializer, CheckInBulkSerializer,
    TodayCheckInsSerializer
)

class GoalListCreateView(generics.ListCreateAPIView):
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return GoalCreateSerializer
        return GoalSerializer
    
    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user).prefetch_related('habits')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Habit.objects.filter(goal__user=self.request.user).select_related('goal')
    
    def perform_create(self, serializer):
        # Ensure the goal belongs to the user
        goal = serializer.validated_data['goal']
        if goal.user != self.request.user:
            raise permissions.PermissionDenied("You can only create habits for your own goals.")
        serializer.save()

class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Habit.objects.filter(goal__user=self.request.user)

class DailyCheckInListCreateView(generics.ListCreateAPIView):
    serializer_class = DailyCheckInSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return DailyCheckIn.objects.filter(habit__goal__user=self.request.user).select_related('habit', 'habit__goal')
    
    def perform_create(self, serializer):
        checkin = serializer.save()
        
        # Update streaks
        checkin.habit.update_streak()

class DailyCheckInDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DailyCheckInSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return DailyCheckIn.objects.filter(habit__goal__user=self.request.user)

class TodayCheckInsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        today = timezone.now().date()
        
        # Get active habits for today
        habits = Habit.objects.filter(
            goal__user=request.user,
            is_active=True,
            goal__is_active=True
        ).select_related('goal')
        
        # Get today's check-ins
        checkins = DailyCheckIn.objects.filter(
            habit__goal__user=request.user,
            date=today
        ).select_related('habit')
        
        serializer = TodayCheckInsSerializer({
            'date': today,
            'habits': habits,
            'completed_checkins': checkins
        })
        
        return Response(serializer.data)

class BulkCheckInView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = CheckInBulkSerializer(data=request.data, many=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        created_checkins = []
        today = timezone.now().date()
        
        for item in serializer.validated_data:
            habit = Habit.objects.get(id=item['habit_id'])
            proof_data = item['proof_data']
            
            # Create check-in based on validation method
            checkin_data = {
                'habit': habit,
                'date': today,
            }
            
            if habit.validation_method == 'photo':
                checkin_data['photo_proof'] = proof_data.get('photo')
            elif habit.validation_method == 'audio':
                checkin_data['audio_proof'] = proof_data.get('audio')
            elif habit.validation_method == 'text':
                checkin_data['text_proof'] = proof_data.get('text')
            elif habit.validation_method == 'screen_recording':
                checkin_data['screen_recording_proof'] = proof_data.get('screen_recording')
            elif habit.validation_method == 'self_report':
                checkin_data['is_self_report'] = True
                checkin_data['self_report_description'] = proof_data.get('description', '')
            
            checkin_serializer = DailyCheckInSerializer(data=checkin_data, context={'request': request})
            if checkin_serializer.is_valid():
                checkin = checkin_serializer.save()
                created_checkins.append(checkin)
        
        return Response(
            DailyCheckInSerializer(created_checkins, many=True).data,
            status=status.HTTP_201_CREATED
        )

class StreakListView(generics.ListAPIView):
    serializer_class = StreakSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Streak.objects.filter(user=self.request.user).select_related('habit', 'habit__goal')

class ProgressInsightListView(generics.ListAPIView):
    serializer_class = ProgressInsightSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ProgressInsight.objects.filter(user=self.request.user).select_related('habit', 'goal')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['hide_sensitive'] = self.request.query_params.get('hide_sensitive', False)
        return context

class MarkInsightReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, insight_id):
        insight = get_object_or_404(ProgressInsight, id=insight_id, user=request.user)
        insight.is_read = True
        insight.save()
        
        return Response({"detail": "Insight marked as read"})

class MilestoneListView(generics.ListAPIView):
    serializer_class = MilestoneSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Milestone.objects.filter(user=self.request.user).select_related('habit', 'goal')

class UserStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        stats, created = UserStats.objects.get_or_create(user=request.user)
        serializer = UserStatsSerializer(stats)
        return Response(serializer.data)

class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        today = timezone.now().date()
        
        # Basic stats
        total_goals = Goal.objects.filter(user=user).count()
        active_goals = Goal.objects.filter(user=user, is_active=True).count()
        total_habits = Habit.objects.filter(goal__user=user).count()
        active_habits = Habit.objects.filter(goal__user=user, is_active=True).count()
        
        # Today's progress
        today_checkins = DailyCheckIn.objects.filter(
            habit__goal__user=user,
            date=today,
            is_approved=True
        ).count()
        
        # Current streaks
        current_streaks = Streak.objects.filter(user=user).order_by('-current_streak')[:5]
        
        # Recent insights
        recent_insights = ProgressInsight.objects.filter(user=user).order_by('-generated_at')[:3]
        
        # Upcoming milestones
        upcoming_milestones = Milestone.objects.filter(
            user=user,
            is_achieved=False
        ).order_by('target_value')[:5]
        
        return Response({
            'stats': {
                'total_goals': total_goals,
                'active_goals': active_goals,
                'total_habits': total_habits,
                'active_habits': active_habits,
                'today_completions': today_checkins,
            },
            'current_streaks': StreakSerializer(current_streaks, many=True).data,
            'recent_insights': ProgressInsightSerializer(recent_insights, many=True).data,
            'upcoming_milestones': MilestoneSerializer(upcoming_milestones, many=True).data,
        })

class CalendarView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, year, month):
        import calendar
        from datetime import date
        
        # Get all check-ins for the month
        checkins = DailyCheckIn.objects.filter(
            habit__goal__user=request.user,
            date__year=year,
            date__month=month,
            is_approved=True
        ).select_related('habit')
        
        # Create calendar data
        cal = calendar.Calendar()
        month_days = cal.monthdayscalendar(year, month)
        
        calendar_data = []
        for week in month_days:
            week_data = []
            for day in week:
                if day == 0:  # Day belongs to previous/next month
                    week_data.append(None)
                else:
                    day_date = date(year, month, day)
                    day_checkins = [c for c in checkins if c.date == day_date]
                    week_data.append({
                        'day': day,
                        'checkins_count': len(day_checkins),
                        'habits_completed': [c.habit.title for c in day_checkins],
                        'is_today': day_date == timezone.now().date()
                    })
            calendar_data.append(week_data)
        
        return Response({
            'year': year,
            'month': month,
            'calendar': calendar_data,
            'total_completions': checkins.count()
        })
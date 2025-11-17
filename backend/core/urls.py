from django.urls import path
from . import views

urlpatterns = [
    # Goals
    path('goals/', views.GoalListCreateView.as_view(), name='goal-list'),
    path('goals/<int:pk>/', views.GoalDetailView.as_view(), name='goal-detail'),
    
    # Habits
    path('habits/', views.HabitListCreateView.as_view(), name='habit-list'),
    path('habits/<int:pk>/', views.HabitDetailView.as_view(), name='habit-detail'),
    
    # Check-ins
    path('checkins/', views.DailyCheckInListCreateView.as_view(), name='checkin-list'),
    path('checkins/<int:pk>/', views.DailyCheckInDetailView.as_view(), name='checkin-detail'),
    path('checkins/today/', views.TodayCheckInsView.as_view(), name='today-checkins'),
    path('checkins/bulk/', views.BulkCheckInView.as_view(), name='bulk-checkin'),
    
    # Streaks
    path('streaks/', views.StreakListView.as_view(), name='streak-list'),
    
    # Insights
    path('insights/', views.ProgressInsightListView.as_view(), name='insight-list'),
    path('insights/<int:insight_id>/read/', views.MarkInsightReadView.as_view(), name='mark-insight-read'),
    
    # Milestones
    path('milestones/', views.MilestoneListView.as_view(), name='milestone-list'),
    
    # Stats & Dashboard
    path('stats/', views.UserStatsView.as_view(), name='user-stats'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('calendar/<int:year>/<int:month>/', views.CalendarView.as_view(), name='calendar'),
]
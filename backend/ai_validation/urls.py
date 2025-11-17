from django.urls import path
from . import views

urlpatterns = [
    # Validation endpoints
    path('validate/', views.ValidateCheckInView.as_view(), name='validate-checkin'),
    path('validate/manual/', views.ManualValidationView.as_view(), name='manual-validation'),
    path('validate/retry/<int:log_id>/', views.RetryFailedValidationView.as_view(), name='retry-validation'),
    
    # Insights generation
    path('insights/generate/', views.GenerateInsightsView.as_view(), name='generate-insights'),
    
    # Feedback
    path('feedback/', views.AIFeedbackCreateView.as_view(), name='ai-feedback'),
    
    # Logs and metrics
    path('logs/', views.UserValidationLogsView.as_view(), name='user-validation-logs'),
    path('performance/', views.AIPerformanceView.as_view(), name='ai-performance'),
    
    # Cache management
    path('cache/clear/', views.ClearValidationCacheView.as_view(), name='clear-cache'),
]
from django.urls import path
from . import views

app_name = 'ai'

urlpatterns = [
    path('validate-checkin/', views.ValidateCheckInView.as_view(), name='validate-checkin'),
    path('manual-validation/', views.ManualValidationView.as_view(), name='manual-validation'),
    path('generate-insights/', views.GenerateInsightsView.as_view(), name='generate-insights'),
    path('ai-feedback/', views.AIFeedbackCreateView.as_view(), name='ai-feedback-list'),
    path('validation-logs/', views.UserValidationLogsView.as_view(), name='validation-logs'),
    path('ai-performance/', views.AIPerformanceView.as_view(), name='ai-performance'),
    path('clear-cache/', views.ClearValidationCacheView.as_view(), name='clear-cache'),
    path('retry-validation/<int:log_id>/', views.RetryFailedValidationView.as_view(), name='retry-validation'),
]

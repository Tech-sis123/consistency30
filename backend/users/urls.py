from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('check-auth/', views.CheckAuthView.as_view(), name='check-auth'),
    
    # User management
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', views.UserUpdateView.as_view(), name='user-update'),
    path('change-password/', views.PasswordChangeView.as_view(), name='change-password'),
    path('delete-account/', views.DeleteAccountView.as_view(), name='delete-account'),
    
    # Onboarding
    path('onboarding/', views.OnboardingView.as_view(), name='onboarding'),
    
    # Profile & Settings
    path('profile/detail/', views.UserProfileDetailView.as_view(), name='profile-detail'),
    path('settings/', views.UserSettingsView.as_view(), name='user-settings'),
    
    # Accountability Partners
    path('partners/', views.AccountabilityPartnerListView.as_view(), name='partner-list'),
    path('partners/add/', views.AddAccountabilityPartnerView.as_view(), name='add-partner'),
    path('partners/<int:pk>/remove/', views.RemoveAccountabilityPartnerView.as_view(), name='remove-partner'),
]
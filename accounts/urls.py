from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', views.UserRegistrationView.as_view(), name='user_register'),
    path('auth/logout/', views.LogoutView.as_view(), name='user_logout'),
    
    # Profile management
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('profile/doctor/', views.DoctorProfileView.as_view(), name='doctor_profile'),
    path('profile/patient/', views.PatientProfileView.as_view(), name='patient_profile'),
    path('profile/change-password/', views.PasswordChangeView.as_view(), name='change_password'),
    
    # Doctor endpoints
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
    path('doctors/<int:id>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    
    # User statistics
    path('stats/', views.user_stats, name='user_stats'),
]


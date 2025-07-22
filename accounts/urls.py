from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
    path('doctors/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('patient/profile/', views.patient_profile, name='patient_profile'),
    path('patient/profile/update/', views.update_patient_profile, name='update_patient_profile'),
]


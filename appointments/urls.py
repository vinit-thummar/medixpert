from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_appointment, name='book_appointment'),
    path('my-appointments/', views.user_appointments, name='user_appointments'),
    path('<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('<int:appointment_id>/update/', views.update_appointment, name='update_appointment'),
    path('<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('doctor/<int:doctor_id>/availability/', views.doctor_availability, name='doctor_availability'),
    path('doctor/<int:doctor_id>/slots/', views.available_time_slots, name='available_time_slots'),
    path('<int:appointment_id>/review/', views.create_review, name='create_review'),
    path('doctor/<int:doctor_id>/reviews/', views.doctor_reviews, name='doctor_reviews'),
]


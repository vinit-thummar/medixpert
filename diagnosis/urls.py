from django.urls import path
from . import views

urlpatterns = [
    path('symptoms/', views.available_symptoms, name='available_symptoms'),
    path('predict/', views.predict_disease, name='predict_disease'),
    path('history/', views.diagnosis_history, name='diagnosis_history'),
    path('history/<int:diagnosis_id>/', views.diagnosis_detail, name='diagnosis_detail'),
    path('analytics/', views.diagnosis_analytics, name='diagnosis_analytics'),
    path('symptoms/all/', views.SymptomListView.as_view(), name='symptom_list'),
    path('diseases/', views.DiseaseListView.as_view(), name='disease_list'),
]


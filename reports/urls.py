from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_report, name='upload_report'),
    path('my-reports/', views.user_reports, name='user_reports'),
    path('<int:report_id>/', views.report_detail, name='report_detail'),
    path('<int:report_id>/update/', views.update_report, name='update_report'),
    path('<int:report_id>/delete/', views.delete_report, name='delete_report'),
    path('types/', views.report_types, name='report_types'),
    path('analytics/', views.reports_analytics, name='reports_analytics'),
    path('<int:report_id>/analyze/', views.create_report_analysis, name='create_report_analysis'),
    path('pending-analysis/', views.pending_reports_for_analysis, name='pending_reports_for_analysis'),
]


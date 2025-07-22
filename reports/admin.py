from django.contrib import admin
from .models import MedicalReport, ReportAnalysis

@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'patient', 'report_type', 'report_date', 'uploaded_by', 'created_at']
    list_filter = ['report_type', 'report_date', 'created_at']
    search_fields = ['title', 'patient__user__username', 'uploaded_by__username']
    readonly_fields = ['file_size', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Report Information', {
            'fields': ('title', 'report_type', 'description', 'report_date')
        }),
        ('File Details', {
            'fields': ('file', 'file_size')
        }),
        ('Associations', {
            'fields': ('patient', 'uploaded_by', 'doctor')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(ReportAnalysis)
class ReportAnalysisAdmin(admin.ModelAdmin):
    list_display = ['report', 'analyzed_by', 'urgency_level', 'follow_up_required', 'created_at']
    list_filter = ['urgency_level', 'follow_up_required', 'created_at']
    search_fields = ['report__title', 'analyzed_by__user__username', 'findings']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Analysis Details', {
            'fields': ('report', 'analyzed_by', 'urgency_level', 'follow_up_required')
        }),
        ('Findings', {
            'fields': ('findings', 'recommendations')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


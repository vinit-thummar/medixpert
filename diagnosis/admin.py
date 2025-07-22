from django.contrib import admin
from .models import Symptom, Disease, DiagnosisHistory

@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'severity_level', 'created_at']
    list_filter = ['severity_level', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['symptoms']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'severity_level')
        }),
        ('Symptoms', {
            'fields': ('symptoms',)
        }),
        ('Additional Information', {
            'fields': ('treatment_info', 'prevention_tips')
        }),
    )

@admin.register(DiagnosisHistory)
class DiagnosisHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'predicted_disease', 'confidence_score', 'created_at']
    list_filter = ['predicted_disease', 'confidence_score', 'created_at']
    search_fields = ['user__username', 'predicted_disease__name']
    readonly_fields = ['created_at']
    filter_horizontal = ['symptoms']
    
    fieldsets = (
        ('Diagnosis Information', {
            'fields': ('user', 'predicted_disease', 'confidence_score')
        }),
        ('Symptoms', {
            'fields': ('symptoms',)
        }),
        ('Additional Notes', {
            'fields': ('additional_notes',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )


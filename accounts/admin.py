from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Doctor, Patient

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'date_of_birth', 'address', 'profile_picture')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'email', 'first_name', 'last_name')
        }),
    )

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'years_of_experience', 'consultation_fee', 'rating', 'is_available', 'city']
    list_filter = ['specialization', 'is_available', 'city', 'state']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'specialization', 'license_number']
    readonly_fields = ['rating', 'total_reviews']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'specialization', 'license_number', 'years_of_experience')
        }),
        ('Professional Details', {
            'fields': ('consultation_fee', 'bio', 'rating', 'total_reviews', 'is_available')
        }),
        ('Location', {
            'fields': ('city', 'state', 'country')
        }),
    )

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'blood_group', 'emergency_contact']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'blood_group']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'emergency_contact', 'blood_group')
        }),
        ('Medical Information', {
            'fields': ('allergies', 'medical_history')
        }),
    )


from django.contrib import admin
from .models import Appointment, DoctorAvailability, Review

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date', 'appointment_time', 'appointment_type', 'status']
    list_filter = ['appointment_type', 'status', 'appointment_date', 'created_at']
    search_fields = ['patient__user__username', 'doctor__user__username', 'reason_for_visit']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('patient', 'doctor', 'appointment_date', 'appointment_time', 'appointment_type', 'status')
        }),
        ('Visit Information', {
            'fields': ('reason_for_visit', 'notes', 'prescription')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'get_day_of_week_display', 'start_time', 'end_time', 'is_available']
    list_filter = ['day_of_week', 'is_available', 'doctor__specialization']
    search_fields = ['doctor__user__username', 'doctor__user__first_name', 'doctor__user__last_name']
    
    fieldsets = (
        ('Doctor', {
            'fields': ('doctor',)
        }),
        ('Availability', {
            'fields': ('day_of_week', 'start_time', 'end_time', 'is_available')
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['appointment__patient__user__username', 'appointment__doctor__user__username', 'comment']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Review Details', {
            'fields': ('appointment', 'rating', 'comment')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )


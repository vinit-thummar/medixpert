from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Patient, Doctor

User = get_user_model()

class MedicalReport(models.Model):
    REPORT_TYPE_CHOICES = [
        ('lab_test', 'Lab Test'),
        ('x_ray', 'X-Ray'),
        ('mri', 'MRI'),
        ('ct_scan', 'CT Scan'),
        ('ultrasound', 'Ultrasound'),
        ('blood_test', 'Blood Test'),
        ('prescription', 'Prescription'),
        ('discharge_summary', 'Discharge Summary'),
        ('other', 'Other'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_reports')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_reports')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='patient_reports')
    
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    
    file = models.FileField(upload_to='medical_reports/')
    file_size = models.PositiveIntegerField(help_text="File size in bytes")
    
    report_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-report_date', '-created_at']
    
    def __str__(self):
        return f"{self.patient.user.username} - {self.title} ({self.report_date})"

class ReportAnalysis(models.Model):
    report = models.OneToOneField(MedicalReport, on_delete=models.CASCADE, related_name='analysis')
    analyzed_by = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='analyzed_reports')
    
    findings = models.TextField()
    recommendations = models.TextField(blank=True, null=True)
    follow_up_required = models.BooleanField(default=False)
    urgency_level = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('urgent', 'Urgent'),
        ],
        default='low'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analysis of {self.report.title} by Dr. {self.analyzed_by.user.last_name}"


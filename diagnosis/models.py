from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Symptom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Disease(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    symptoms = models.ManyToManyField(Symptom, related_name='diseases')
    severity_level = models.CharField(
        max_length=20,
        choices=[
            ('mild', 'Mild'),
            ('moderate', 'Moderate'),
            ('severe', 'Severe'),
            ('critical', 'Critical'),
        ],
        default='mild'
    )
    treatment_info = models.TextField(blank=True, null=True)
    prevention_tips = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class DiagnosisHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diagnosis_history')
    symptoms = models.ManyToManyField(Symptom)
    predicted_disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=4)
    additional_notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Diagnosis Histories"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.predicted_disease.name} ({self.confidence_score})"


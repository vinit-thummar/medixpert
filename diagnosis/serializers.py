from rest_framework import serializers
from .models import Symptom, Disease, DiagnosisHistory

class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = ['id', 'name', 'description', 'category']

class DiseaseSerializer(serializers.ModelSerializer):
    symptoms = SymptomSerializer(many=True, read_only=True)
    
    class Meta:
        model = Disease
        fields = ['id', 'name', 'description', 'symptoms', 'severity_level', 'treatment_info', 'prevention_tips']

class DiagnosisHistorySerializer(serializers.ModelSerializer):
    symptoms = SymptomSerializer(many=True, read_only=True)
    predicted_disease = DiseaseSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = DiagnosisHistory
        fields = ['id', 'user', 'symptoms', 'predicted_disease', 'confidence_score', 'additional_notes', 'created_at']

class DiseasePredictionSerializer(serializers.Serializer):
    symptoms = serializers.ListField(
        child=serializers.CharField(max_length=100),
        min_length=1,
        help_text="List of symptoms for disease prediction"
    )
    additional_notes = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    def validate_symptoms(self, value):
        if not value:
            raise serializers.ValidationError("At least one symptom is required")
        return value


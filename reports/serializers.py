from rest_framework import serializers
from .models import MedicalReport, ReportAnalysis
from accounts.serializers import PatientProfileSerializer, DoctorProfileSerializer

class MedicalReportSerializer(serializers.ModelSerializer):
    patient = PatientProfileSerializer(read_only=True)
    uploaded_by = serializers.StringRelatedField(read_only=True)
    doctor = DoctorProfileSerializer(read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = MedicalReport
        fields = [
            'id', 'patient', 'uploaded_by', 'doctor', 'title', 'report_type', 
            'description', 'file', 'file_url', 'file_size', 'report_date', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'uploaded_by', 'file_size', 'created_at', 'updated_at']
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None

class MedicalReportUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalReport
        fields = ['title', 'report_type', 'description', 'file', 'report_date']
    
    def validate_file(self, value):
        # Check file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size cannot exceed 10MB")
        
        # Check file type
        allowed_types = ['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx']
        file_extension = value.name.split('.')[-1].lower()
        if file_extension not in allowed_types:
            raise serializers.ValidationError(
                f"File type '{file_extension}' not allowed. Allowed types: {', '.join(allowed_types)}"
            )
        
        return value

class ReportAnalysisSerializer(serializers.ModelSerializer):
    report = MedicalReportSerializer(read_only=True)
    analyzed_by = DoctorProfileSerializer(read_only=True)
    
    class Meta:
        model = ReportAnalysis
        fields = [
            'id', 'report', 'analyzed_by', 'findings', 'recommendations', 
            'follow_up_required', 'urgency_level', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'analyzed_by', 'created_at', 'updated_at']


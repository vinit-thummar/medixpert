from rest_framework import serializers
from .models import Appointment, DoctorAvailability, Review
from accounts.serializers import DoctorSerializer, PatientSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    doctor_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'doctor', 'doctor_id', 'appointment_date', 
            'appointment_time', 'appointment_type', 'status', 'reason_for_visit', 
            'notes', 'prescription', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'patient', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        # Check if the appointment slot is available
        doctor_id = attrs.get('doctor_id')
        appointment_date = attrs.get('appointment_date')
        appointment_time = attrs.get('appointment_time')
        
        if doctor_id and appointment_date and appointment_time:
            existing_appointment = Appointment.objects.filter(
                doctor_id=doctor_id,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status__in=['scheduled', 'confirmed']
            ).exclude(id=self.instance.id if self.instance else None)
            
            if existing_appointment.exists():
                raise serializers.ValidationError("This appointment slot is already booked")
        
        return attrs

class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = DoctorAvailability
        fields = ['id', 'doctor', 'day_of_week', 'day_name', 'start_time', 'end_time', 'is_available']

class ReviewSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer(read_only=True)
    patient_name = serializers.CharField(source='appointment.patient.user.get_full_name', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'appointment', 'patient_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']

class AppointmentBookingSerializer(serializers.Serializer):
    doctor_id = serializers.IntegerField()
    appointment_date = serializers.DateField()
    appointment_time = serializers.TimeField()
    appointment_type = serializers.ChoiceField(choices=Appointment.APPOINTMENT_TYPE_CHOICES, default='consultation')
    reason_for_visit = serializers.CharField(max_length=500)
    
    def validate_doctor_id(self, value):
        from accounts.models import Doctor
        try:
            doctor = Doctor.objects.get(id=value, is_available=True)
            return value
        except Doctor.DoesNotExist:
            raise serializers.ValidationError("Doctor not found or not available")
    
    def validate(self, attrs):
        doctor_id = attrs.get('doctor_id')
        appointment_date = attrs.get('appointment_date')
        appointment_time = attrs.get('appointment_time')
        
        # Check if appointment is in the future
        from datetime import datetime, date, time
        appointment_datetime = datetime.combine(appointment_date, appointment_time)
        if appointment_datetime <= datetime.now():
            raise serializers.ValidationError("Appointment must be scheduled for a future date and time")
        
        # Check if the slot is available
        existing_appointment = Appointment.objects.filter(
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status__in=['scheduled', 'confirmed']
        )
        
        if existing_appointment.exists():
            raise serializers.ValidationError("This appointment slot is already booked")
        
        return attrs


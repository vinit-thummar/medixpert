from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from .models import Appointment, DoctorAvailability, Review
from .serializers import (
    AppointmentSerializer, DoctorAvailabilitySerializer, 
    ReviewSerializer, AppointmentBookingSerializer
)
from accounts.models import Doctor, Patient

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_appointment(request):
    """Book a new appointment"""
    serializer = AppointmentBookingSerializer(data=request.data)
    
    if serializer.is_valid():
        # Get patient profile
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return Response(
                {'error': 'Patient profile not found. Please complete your profile first.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get doctor
        doctor = get_object_or_404(Doctor, id=serializer.validated_data['doctor_id'])
        
        # Create appointment
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=serializer.validated_data['appointment_date'],
            appointment_time=serializer.validated_data['appointment_time'],
            appointment_type=serializer.validated_data['appointment_type'],
            reason_for_visit=serializer.validated_data['reason_for_visit'],
            status='scheduled'
        )
        
        # Send confirmation email (in development, this will print to console)
        try:
            send_mail(
                subject='Appointment Confirmation - MediXpert',
                message=f'''
                Dear {patient.user.get_full_name()},
                
                Your appointment has been successfully booked with Dr. {doctor.user.get_full_name()}.
                
                Appointment Details:
                - Date: {appointment.appointment_date}
                - Time: {appointment.appointment_time}
                - Type: {appointment.get_appointment_type_display()}
                - Reason: {appointment.reason_for_visit}
                
                Please arrive 15 minutes before your scheduled time.
                
                Best regards,
                MediXpert Team
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@medixpert.com',
                recipient_list=[patient.user.email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Email sending failed: {e}")
        
        return Response({
            'message': 'Appointment booked successfully',
            'appointment': AppointmentSerializer(appointment).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_appointments(request):
    """Get user's appointments"""
    try:
        patient = Patient.objects.get(user=request.user)
        appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date', '-appointment_time')
        
        # Filter by status if provided
        status_filter = request.query_params.get('status')
        if status_filter:
            appointments = appointments.filter(status=status_filter)
        
        serializer = AppointmentSerializer(appointments, many=True)
        return Response({
            'appointments': serializer.data,
            'total_count': appointments.count()
        })
    except Patient.DoesNotExist:
        return Response({'error': 'Patient profile not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def appointment_detail(request, appointment_id):
    """Get appointment details"""
    try:
        patient = Patient.objects.get(user=request.user)
        appointment = get_object_or_404(Appointment, id=appointment_id, patient=patient)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)
    except Patient.DoesNotExist:
        return Response({'error': 'Patient profile not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_appointment(request, appointment_id):
    """Update appointment (cancel, reschedule)"""
    try:
        patient = Patient.objects.get(user=request.user)
        appointment = get_object_or_404(Appointment, id=appointment_id, patient=patient)
        
        # Only allow updates for scheduled or confirmed appointments
        if appointment.status not in ['scheduled', 'confirmed']:
            return Response(
                {'error': 'Cannot modify this appointment'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Appointment updated successfully',
                'appointment': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Patient.DoesNotExist:
        return Response({'error': 'Patient profile not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancel_appointment(request, appointment_id):
    """Cancel an appointment"""
    try:
        patient = Patient.objects.get(user=request.user)
        appointment = get_object_or_404(Appointment, id=appointment_id, patient=patient)
        
        if appointment.status in ['completed', 'cancelled']:
            return Response(
                {'error': 'Cannot cancel this appointment'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        appointment.status = 'cancelled'
        appointment.save()
        
        return Response({'message': 'Appointment cancelled successfully'})
    except Patient.DoesNotExist:
        return Response({'error': 'Patient profile not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_availability(request, doctor_id):
    """Get doctor's availability"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    availability = DoctorAvailability.objects.filter(doctor=doctor, is_available=True)
    serializer = DoctorAvailabilitySerializer(availability, many=True)
    
    # Get booked slots for the next 30 days
    from datetime import date
    end_date = date.today() + timedelta(days=30)
    booked_slots = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__range=[date.today(), end_date],
        status__in=['scheduled', 'confirmed']
    ).values('appointment_date', 'appointment_time')
    
    return Response({
        'availability': serializer.data,
        'booked_slots': list(booked_slots)
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_time_slots(request, doctor_id):
    """Get available time slots for a specific doctor and date"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    date_str = request.query_params.get('date')
    
    if not date_str:
        return Response({'error': 'Date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get doctor's availability for the day
    day_of_week = appointment_date.weekday()
    availability = DoctorAvailability.objects.filter(
        doctor=doctor,
        day_of_week=day_of_week,
        is_available=True
    ).first()
    
    if not availability:
        return Response({'available_slots': []})
    
    # Generate time slots (30-minute intervals)
    from datetime import time, timedelta
    slots = []
    current_time = datetime.combine(appointment_date, availability.start_time)
    end_time = datetime.combine(appointment_date, availability.end_time)
    
    while current_time < end_time:
        slots.append(current_time.time())
        current_time += timedelta(minutes=30)
    
    # Remove booked slots
    booked_times = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=appointment_date,
        status__in=['scheduled', 'confirmed']
    ).values_list('appointment_time', flat=True)
    
    available_slots = [slot for slot in slots if slot not in booked_times]
    
    return Response({
        'available_slots': [slot.strftime('%H:%M') for slot in available_slots],
        'date': date_str
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, appointment_id):
    """Create a review for a completed appointment"""
    try:
        patient = Patient.objects.get(user=request.user)
        appointment = get_object_or_404(
            Appointment, 
            id=appointment_id, 
            patient=patient, 
            status='completed'
        )
        
        # Check if review already exists
        if hasattr(appointment, 'review'):
            return Response(
                {'error': 'Review already exists for this appointment'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(appointment=appointment)
            
            # Update doctor's rating
            doctor = appointment.doctor
            reviews = Review.objects.filter(appointment__doctor=doctor)
            total_rating = sum(r.rating for r in reviews)
            doctor.rating = total_rating / reviews.count()
            doctor.total_reviews = reviews.count()
            doctor.save()
            
            return Response({
                'message': 'Review created successfully',
                'review': ReviewSerializer(review).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Patient.DoesNotExist:
        return Response({'error': 'Patient profile not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_reviews(request, doctor_id):
    """Get reviews for a specific doctor"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    reviews = Review.objects.filter(appointment__doctor=doctor).order_by('-created_at')
    
    # Pagination
    page_size = int(request.query_params.get('page_size', 10))
    page = int(request.query_params.get('page', 1))
    start = (page - 1) * page_size
    end = start + page_size
    
    paginated_reviews = reviews[start:end]
    serializer = ReviewSerializer(paginated_reviews, many=True)
    
    return Response({
        'reviews': serializer.data,
        'total_count': reviews.count(),
        'average_rating': doctor.rating,
        'total_reviews': doctor.total_reviews,
        'page': page,
        'page_size': page_size,
        'has_next': end < reviews.count()
    })


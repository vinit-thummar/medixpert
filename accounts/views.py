from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import transaction
from django.core.cache import cache
from rest_framework.filters import SearchFilter, OrderingFilter
import logging

from .models import User, Doctor, Patient
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserRegistrationSerializer,
    UserProfileSerializer,
    DoctorProfileSerializer,
    PatientProfileSerializer,
    DoctorListSerializer,
    PasswordChangeSerializer
)

logger = logging.getLogger(__name__)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT login view with enhanced error handling"""
    
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                logger.info(f"User {request.data.get('username')} logged in successfully")
            return response
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return Response(
                {'error': 'Login failed. Please check your credentials.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserRegistrationView(APIView):
    """Enhanced user registration with transaction support"""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        try:
            with transaction.atomic():
                serializer = UserRegistrationSerializer(data=request.data)
                if serializer.is_valid():
                    user = serializer.save()
                    
                    # Generate tokens for immediate login
                    refresh = RefreshToken.for_user(user)
                    access_token = refresh.access_token
                    
                    # Add custom claims
                    access_token['user_type'] = user.user_type
                    access_token['email'] = user.email
                    
                    logger.info(f"New user registered: {user.username}")
                    
                    return Response({
                        'message': 'Registration successful',
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'user_type': user.user_type,
                        },
                        'tokens': {
                            'access': str(access_token),
                            'refresh': str(refresh),
                        }
                    }, status=status.HTTP_201_CREATED)
                
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return Response(
                {'error': 'Registration failed. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """User profile view with caching"""
    
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        # Try to get from cache first
        cache_key = f"user_profile_{request.user.id}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        response = super().retrieve(request, *args, **kwargs)
        
        # Cache the response for 15 minutes
        cache.set(cache_key, response.data, 900)
        
        return response
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        
        # Clear cache after update
        cache_key = f"user_profile_{request.user.id}"
        cache.delete(cache_key)
        
        logger.info(f"User profile updated: {request.user.username}")
        
        return response


class DoctorProfileView(generics.RetrieveUpdateAPIView):
    """Doctor profile management"""
    
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        if self.request.user.user_type != 'doctor':
            raise permissions.PermissionDenied("Only doctors can access this endpoint")
        return self.request.user.doctor_profile
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        
        # Clear related caches
        cache.delete(f"doctor_profile_{request.user.id}")
        cache.delete("doctors_list")
        
        return response


class PatientProfileView(generics.RetrieveUpdateAPIView):
    """Patient profile management"""
    
    serializer_class = PatientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        if self.request.user.user_type != 'patient':
            raise permissions.PermissionDenied("Only patients can access this endpoint")
        return self.request.user.patient_profile


class DoctorListView(generics.ListAPIView):
    """Enhanced doctor listing with filtering and search"""
    
    serializer_class = DoctorListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_fields = ['specialization', 'city', 'state', 'is_available']
    search_fields = ['user__first_name', 'user__last_name', 'specialization', 'city']
    ordering_fields = ['rating', 'years_of_experience', 'consultation_fee']
    ordering = ['-rating', '-years_of_experience']
    
    def get_queryset(self):
        # Try to get from cache first
        cache_key = "doctors_list"
        cached_queryset = cache.get(cache_key)
        
        if cached_queryset is None:
            queryset = Doctor.objects.select_related('user').filter(
                user__is_active=True
            )
            # Cache for 30 minutes
            cache.set(cache_key, queryset, 1800)
            return queryset
        
        return cached_queryset


class DoctorDetailView(generics.RetrieveAPIView):
    """Doctor detail view with caching"""
    
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Doctor.objects.select_related('user').filter(
            user__is_active=True
        )
    
    def retrieve(self, request, *args, **kwargs):
        doctor_id = kwargs.get('id')
        cache_key = f"doctor_detail_{doctor_id}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        response = super().retrieve(request, *args, **kwargs)
        
        # Cache for 1 hour
        cache.set(cache_key, response.data, 3600)
        
        return response


class PasswordChangeView(APIView):
    """Password change endpoint"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Password changed for user: {request.user.username}")
            
            return Response({
                'message': 'Password changed successfully'
            }, status=status.HTTP_200_OK)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(APIView):
    """Enhanced logout with token blacklisting"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            # Clear user-related caches
            cache.delete(f"user_profile_{request.user.id}")
            if hasattr(request.user, 'doctor_profile'):
                cache.delete(f"doctor_profile_{request.user.id}")
            
            logger.info(f"User logged out: {request.user.username}")
            
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            return Response({
                'error': 'Logout failed'
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """Get user statistics"""
    try:
        user = request.user
        cache_key = f"user_stats_{user.id}"
        cached_stats = cache.get(cache_key)
        
        if cached_stats:
            return Response(cached_stats)
        
        stats = {
            'total_diagnoses': 0,
            'upcoming_appointments': 0,
            'medical_reports': 0,
            'health_score': 85  # Default score
        }
        
        if user.user_type == 'patient':
            # Get patient-specific stats
            from diagnosis.models import Diagnosis
            from appointments.models import Appointment
            from reports.models import MedicalReport
            
            stats['total_diagnoses'] = Diagnosis.objects.filter(
                patient=user.patient_profile
            ).count()
            
            stats['upcoming_appointments'] = Appointment.objects.filter(
                patient=user.patient_profile,
                status='scheduled'
            ).count()
            
            stats['medical_reports'] = MedicalReport.objects.filter(
                patient=user.patient_profile
            ).count()
        
        elif user.user_type == 'doctor':
            # Get doctor-specific stats
            from appointments.models import Appointment
            
            stats = {
                'total_patients': Appointment.objects.filter(
                    doctor=user.doctor_profile
                ).values('patient').distinct().count(),
                
                'upcoming_appointments': Appointment.objects.filter(
                    doctor=user.doctor_profile,
                    status='scheduled'
                ).count(),
                
                'completed_appointments': Appointment.objects.filter(
                    doctor=user.doctor_profile,
                    status='completed'
                ).count(),
                
                'rating': float(user.doctor_profile.rating)
            }
        
        # Cache for 10 minutes
        cache.set(cache_key, stats, 600)
        
        return Response(stats)
    
    except Exception as e:
        logger.error(f"Error getting user stats: {str(e)}")
        return Response(
            {'error': 'Failed to get user statistics'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


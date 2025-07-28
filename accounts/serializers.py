from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, Doctor, Patient


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer with additional user data"""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token["user_type"] = user.user_type
        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add user data to response
        data.update({
            "user": {
                "id": self.user.id,
                "username": self.user.username,
                "email": self.user.email,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "user_type": self.user.user_type,
                "is_active": self.user.is_active,
            }
        })
        
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Enhanced user registration serializer with validation"""
    
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(
        write_only=True,
    )
    
    # Doctor specific fields
    license_number = serializers.CharField(required=False, allow_blank=True)
    years_of_experience = serializers.IntegerField(required=False)
    consultation_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    specialization = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    state = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "username", "email", "password", "confirm_password",
            "first_name", "last_name", "user_type", "phone_number",
            "license_number", "years_of_experience", "consultation_fee",
            "specialization", "city", "state"
        ]
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords don\\\'t match")
        
        if attrs.get("user_type") == "doctor":
            if not attrs.get("license_number"):
                raise serializers.ValidationError({"license_number": "This field is required for doctors."}) 
            if not attrs.get("years_of_experience"):
                raise serializers.ValidationError({"years_of_experience": "This field is required for doctors."}) 
            if not attrs.get("consultation_fee"):
                raise serializers.ValidationError({"consultation_fee": "This field is required for doctors."}) 
            if not attrs.get("specialization"):
                raise serializers.ValidationError({"specialization": "This field is required for doctors."}) 
            if not attrs.get("city"):
                raise serializers.ValidationError({"city": "This field is required for doctors."}) 
            if not attrs.get("state"):
                raise serializers.ValidationError({"state": "This field is required for doctors."}) 

        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user_type = validated_data.pop("user_type")
        
        user = User.objects.create_user(user_type=user_type, **validated_data)
        
        # Create profile based on user type
        if user_type == "patient":
            Patient.objects.create(user=user)
        elif user_type == "doctor":
            Doctor.objects.create(
                user=user,
                specialization=validated_data.get("specialization", "General Medicine"),
                license_number=validated_data.get("license_number"),
                years_of_experience=validated_data.get("years_of_experience"),
                consultation_fee=validated_data.get("consultation_fee"),
                city=validated_data.get("city", "Not specified"),
                state=validated_data.get("state", "Not specified")
            )
        
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer for updates"""
    
    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "user_type", "phone_number", "is_active", "date_joined"
        ]
        read_only_fields = ["id", "username", "user_type", "date_joined"]

    def validate_email(self, value):
        user = self.context["request"].user
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Email already exists")
        return value


class DoctorProfileSerializer(serializers.ModelSerializer):
    """Doctor profile serializer"""
    
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Doctor
        fields = [
            "user", "specialization", "license_number", "years_of_experience",
            "consultation_fee", "bio", "rating", "total_reviews", "is_available",
            "city", "state", "country", "created_at", "updated_at"
        ]
        read_only_fields = ["rating", "total_reviews", "created_at", "updated_at"]


class PatientProfileSerializer(serializers.ModelSerializer):
    """Patient profile serializer"""
    
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            "user", "emergency_contact", "blood_group", "allergies",
            "medical_history", "created_at", "updated_at"
        ]
        read_only_fields = ["created_at", "updated_at"]


class DoctorListSerializer(serializers.ModelSerializer):
    """Serializer for doctor listing with basic info"""
    
    user = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    
    class Meta:
        model = Doctor
        fields = [
            "id", "user", "full_name", "specialization", "years_of_experience",
            "consultation_fee", "rating", "total_reviews", "is_available",
            "location"
        ]
    
    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
        }
    
    def get_full_name(self, obj):
        return f"Dr. {obj.user.first_name} {obj.user.last_name}"
    
    def get_location(self, obj):
        return f"{obj.city}, {obj.state}"


class PasswordChangeSerializer(serializers.Serializer):
    """Password change serializer"""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("New passwords don\\\'t match")
        return attrs

    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user



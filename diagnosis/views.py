from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Symptom, Disease, DiagnosisHistory
from .serializers import SymptomSerializer, DiseaseSerializer, DiagnosisHistorySerializer, DiseasePredictionSerializer
from .ml_model import get_predictor

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_symptoms(request):
    """Get list of available symptoms for prediction"""
    predictor = get_predictor()
    symptoms = predictor.get_available_symptoms()
    
    # Format symptoms for frontend
    formatted_symptoms = [
        {
            'id': i,
            'name': symptom.replace('_', ' ').title(),
            'value': symptom
        }
        for i, symptom in enumerate(symptoms)
    ]
    
    return Response({
        'symptoms': formatted_symptoms,
        'total_count': len(formatted_symptoms)
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_disease(request):
    """Predict disease based on symptoms"""
    serializer = DiseasePredictionSerializer(data=request.data)
    
    if serializer.is_valid():
        symptoms = serializer.validated_data['symptoms']
        additional_notes = serializer.validated_data.get('additional_notes', '')
        
        # Get prediction from ML model
        predictor = get_predictor()
        prediction_result = predictor.predict_disease(symptoms)
        
        # Get or create disease object
        disease, created = Disease.objects.get_or_create(
            name=prediction_result['predicted_disease'],
            defaults={
                'description': f"Predicted disease based on symptoms: {', '.join(symptoms)}",
                'severity_level': 'moderate'
            }
        )
        
        # Create or get symptom objects
        symptom_objects = []
        for symptom_name in symptoms:
            symptom, created = Symptom.objects.get_or_create(
                name=symptom_name.replace('_', ' ').title(),
                defaults={'description': f'Symptom: {symptom_name.replace("_", " ").title()}'}
            )
            symptom_objects.append(symptom)
        
        # Save diagnosis history
        diagnosis_history = DiagnosisHistory.objects.create(
            user=request.user,
            predicted_disease=disease,
            confidence_score=prediction_result['confidence'],
            additional_notes=additional_notes
        )
        diagnosis_history.symptoms.set(symptom_objects)
        
        # Prepare response
        response_data = {
            'prediction': {
                'disease': disease.name,
                'confidence': round(prediction_result['confidence'] * 100, 2),
                'severity': disease.severity_level,
                'description': disease.description
            },
            'symptoms_analyzed': [s.replace('_', ' ').title() for s in symptoms],
            'recommendations': [
                'Consult with a healthcare professional for proper diagnosis',
                'Monitor your symptoms and seek immediate medical attention if they worsen',
                'Maintain a healthy lifestyle and follow preventive measures'
            ],
            'diagnosis_id': diagnosis_history.id
        }
        
        # Add treatment info if available
        if disease.treatment_info:
            response_data['prediction']['treatment_info'] = disease.treatment_info
        
        # Add prevention tips if available
        if disease.prevention_tips:
            response_data['prediction']['prevention_tips'] = disease.prevention_tips
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def diagnosis_history(request):
    """Get user's diagnosis history"""
    history = DiagnosisHistory.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    page_size = int(request.query_params.get('page_size', 10))
    page = int(request.query_params.get('page', 1))
    start = (page - 1) * page_size
    end = start + page_size
    
    paginated_history = history[start:end]
    serializer = DiagnosisHistorySerializer(paginated_history, many=True)
    
    return Response({
        'results': serializer.data,
        'total_count': history.count(),
        'page': page,
        'page_size': page_size,
        'has_next': end < history.count()
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def diagnosis_detail(request, diagnosis_id):
    """Get detailed information about a specific diagnosis"""
    diagnosis = get_object_or_404(DiagnosisHistory, id=diagnosis_id, user=request.user)
    serializer = DiagnosisHistorySerializer(diagnosis)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def diagnosis_analytics(request):
    """Get analytics data for user's diagnosis history"""
    user_history = DiagnosisHistory.objects.filter(user=request.user)
    
    # Disease frequency
    disease_counts = {}
    for diagnosis in user_history:
        disease_name = diagnosis.predicted_disease.name
        disease_counts[disease_name] = disease_counts.get(disease_name, 0) + 1
    
    # Most common symptoms
    symptom_counts = {}
    for diagnosis in user_history:
        for symptom in diagnosis.symptoms.all():
            symptom_counts[symptom.name] = symptom_counts.get(symptom.name, 0) + 1
    
    # Recent trends (last 30 days)
    from datetime import datetime, timedelta
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_diagnoses = user_history.filter(created_at__gte=thirty_days_ago)
    
    analytics_data = {
        'total_diagnoses': user_history.count(),
        'recent_diagnoses': recent_diagnoses.count(),
        'disease_frequency': [
            {'disease': disease, 'count': count}
            for disease, count in sorted(disease_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        ],
        'common_symptoms': [
            {'symptom': symptom, 'count': count}
            for symptom, count in sorted(symptom_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        ],
        'average_confidence': round(
            sum(d.confidence_score for d in user_history) / max(user_history.count(), 1) * 100, 2
        )
    }
    
    return Response(analytics_data)

class SymptomListView(generics.ListAPIView):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer
    permission_classes = [IsAuthenticated]

class DiseaseListView(generics.ListAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [IsAuthenticated]


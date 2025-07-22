from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import MedicalReport, ReportAnalysis
from .serializers import MedicalReportSerializer, MedicalReportUploadSerializer, ReportAnalysisSerializer
from accounts.models import Patient, Doctor

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_report(request):
    """Upload a medical report"""
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        return Response(
            {'error': 'Patient profile not found. Please complete your profile first.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = MedicalReportUploadSerializer(data=request.data)
    if serializer.is_valid():
        report = serializer.save(
            patient=patient,
            uploaded_by=request.user,
            file_size=request.FILES['file'].size
        )
        
        response_serializer = MedicalReportSerializer(report, context={'request': request})
        return Response({
            'message': 'Medical report uploaded successfully',
            'report': response_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_reports(request):
    """Get user's medical reports"""
    try:
        patient = Patient.objects.get(user=request.user)
        reports = MedicalReport.objects.filter(patient=patient).order_by('-report_date', '-created_at')
        
        # Filter by report type if provided
        report_type = request.query_params.get('type')
        if report_type:
            reports = reports.filter(report_type=report_type)
        
        # Pagination
        page_size = int(request.query_params.get('page_size', 10))
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * page_size
        end = start + page_size
        
        paginated_reports = reports[start:end]
        serializer = MedicalReportSerializer(paginated_reports, many=True, context={'request': request})
        
        return Response({
            'reports': serializer.data,
            'total_count': reports.count(),
            'page': page,
            'page_size': page_size,
            'has_next': end < reports.count()
        })
    except Patient.DoesNotExist:
        return Response({'error': 'Patient profile not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def report_detail(request, report_id):
    """Get detailed information about a specific report"""
    try:
        patient = Patient.objects.get(user=request.user)
        report = get_object_or_404(MedicalReport, id=report_id, patient=patient)
        serializer = MedicalReportSerializer(report, context={'request': request})
        
        # Include analysis if available
        response_data = serializer.data
        if hasattr(report, 'analysis'):
            analysis_serializer = ReportAnalysisSerializer(report.analysis)
            response_data['analysis'] = analysis_serializer.data
        
        return Response(response_data)
    except Patient.DoesNotExist:
        return Response({'error': 'Patient profile not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_report(request, report_id):
    """Update a medical report"""
    try:
        patient = Patient.objects.get(user=request.user)
        report = get_object_or_404(MedicalReport, id=report_id, patient=patient)
        
        serializer = MedicalReportUploadSerializer(report, data=request.data, partial=True)
        if serializer.is_valid():
            # Update file size if new file is uploaded
            if 'file' in request.FILES:
                report.file_size = request.FILES['file'].size
            
            serializer.save()
            response_serializer = MedicalReportSerializer(report, context={'request': request})
            return Response({
                'message': 'Medical report updated successfully',
                'report': response_serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Patient.DoesNotExist:
        return Response({'error': 'Patient profile not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_report(request, report_id):
    """Delete a medical report"""
    try:
        patient = Patient.objects.get(user=request.user)
        report = get_object_or_404(MedicalReport, id=report_id, patient=patient)
        
        # Delete the file from storage
        if report.file:
            report.file.delete()
        
        report.delete()
        return Response({'message': 'Medical report deleted successfully'})
    except Patient.DoesNotExist:
        return Response({'error': 'Patient profile not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def report_types(request):
    """Get available report types"""
    types = [
        {'value': choice[0], 'label': choice[1]} 
        for choice in MedicalReport.REPORT_TYPE_CHOICES
    ]
    return Response({'report_types': types})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reports_analytics(request):
    """Get analytics for user's medical reports"""
    try:
        patient = Patient.objects.get(user=request.user)
        reports = MedicalReport.objects.filter(patient=patient)
        
        # Report type distribution
        type_counts = {}
        for report in reports:
            report_type = report.get_report_type_display()
            type_counts[report_type] = type_counts.get(report_type, 0) + 1
        
        # Recent reports (last 30 days)
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_reports = reports.filter(created_at__gte=thirty_days_ago)
        
        # Reports with analysis
        analyzed_reports = reports.filter(analysis__isnull=False)
        
        analytics_data = {
            'total_reports': reports.count(),
            'recent_reports': recent_reports.count(),
            'analyzed_reports': analyzed_reports.count(),
            'report_type_distribution': [
                {'type': report_type, 'count': count}
                for report_type, count in type_counts.items()
            ],
            'total_file_size': sum(report.file_size for report in reports),
            'average_reports_per_month': reports.count() / max(1, 
                (datetime.now() - reports.first().created_at).days / 30 if reports.exists() else 1
            )
        }
        
        return Response(analytics_data)
    except Patient.DoesNotExist:
        return Response({'error': 'Patient profile not found'}, status=status.HTTP_404_NOT_FOUND)

# Doctor views for report analysis
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_report_analysis(request, report_id):
    """Create analysis for a medical report (Doctor only)"""
    # Check if user is a doctor
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return Response(
            {'error': 'Only doctors can create report analysis'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    report = get_object_or_404(MedicalReport, id=report_id)
    
    # Check if analysis already exists
    if hasattr(report, 'analysis'):
        return Response(
            {'error': 'Analysis already exists for this report'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = ReportAnalysisSerializer(data=request.data)
    if serializer.is_valid():
        analysis = serializer.save(report=report, analyzed_by=doctor)
        return Response({
            'message': 'Report analysis created successfully',
            'analysis': ReportAnalysisSerializer(analysis).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pending_reports_for_analysis(request):
    """Get reports pending analysis (Doctor only)"""
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return Response(
            {'error': 'Only doctors can access this endpoint'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Get reports without analysis
    pending_reports = MedicalReport.objects.filter(analysis__isnull=True).order_by('-created_at')
    
    # Pagination
    page_size = int(request.query_params.get('page_size', 10))
    page = int(request.query_params.get('page', 1))
    start = (page - 1) * page_size
    end = start + page_size
    
    paginated_reports = pending_reports[start:end]
    serializer = MedicalReportSerializer(paginated_reports, many=True, context={'request': request})
    
    return Response({
        'reports': serializer.data,
        'total_count': pending_reports.count(),
        'page': page,
        'page_size': page_size,
        'has_next': end < pending_reports.count()
    })


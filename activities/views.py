from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import (
    ActivityType, StandardQuestion, MaintenanceActivity,
    PartUsage, ActivityPhoto, ActivityAnswer
)
from .serializers import (
    ActivityTypeSerializer, StandardQuestionSerializer,
    MaintenanceActivitySerializer, MaintenanceActivityListSerializer,
    MaintenanceActivityCreateSerializer, ActivityStartSerializer,
    ActivityCompleteSerializer, PhotoUploadSerializer,
    PartUsageSerializer, ActivityPhotoSerializer
)


class ActivityTypeListView(generics.ListAPIView):
    """
    Lista tipos de atividade
    """
    queryset = ActivityType.objects.filter(is_active=True)
    serializer_class = ActivityTypeSerializer
    permission_classes = [IsAuthenticated]


class MaintenanceActivityListCreateView(generics.ListCreateAPIView):
    """
    Lista e cria atividades de manutenção
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location__name']
    ordering_fields = ['created_at', 'scheduled_date', 'priority', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        queryset = MaintenanceActivity.objects.all()
        
        # Filtros por parâmetro
        status_filter = self.request.query_params.get('status')
        priority_filter = self.request.query_params.get('priority')
        technician_filter = self.request.query_params.get('technician')
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        
        if technician_filter:
            queryset = queryset.filter(technician_id=technician_filter)
        
        # Se não for supervisor, mostra apenas suas atividades
        if not (user.is_supervisor or user.is_staff):
            queryset = queryset.filter(technician=user)
        
        return queryset.select_related('technician', 'activity_type', 'location')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MaintenanceActivityCreateSerializer
        return MaintenanceActivityListSerializer


class MaintenanceActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalhe, atualiza e deleta atividade
    """
    serializer_class = MaintenanceActivitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = MaintenanceActivity.objects.all()
        
        # Se não for supervisor, vê apenas suas atividades
        if not (user.is_supervisor or user.is_staff):
            queryset = queryset.filter(technician=user)
        
        return queryset


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_activity(request, activity_id):
    """
    Inicia uma atividade
    """
    try:
        activity = MaintenanceActivity.objects.get(id=activity_id)
    except MaintenanceActivity.DoesNotExist:
        return Response(
            {'error': 'Atividade não encontrada.'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Verifica se o usuário pode iniciar esta atividade
    if not (request.user == activity.technician or request.user.is_supervisor):
        return Response(
            {'error': 'Você não tem permissão para iniciar esta atividade.'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if activity.status != 'pending':
        return Response(
            {'error': f'Atividade não pode ser iniciada. Status atual: {activity.get_status_display()}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = ActivityStartSerializer(data=request.data)
    if serializer.is_valid():
        activity.status = 'in_progress'
        activity.started_at = timezone.now()
        if serializer.validated_data.get('observations'):
            activity.observations = serializer.validated_data['observations']
        activity.save()
        
        return Response({
            'success': True,
            'message': 'Atividade iniciada com sucesso.',
            'activity': MaintenanceActivitySerializer(activity, context={'request': request}).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_activity(request, activity_id):
    """
    Finaliza uma atividade
    """
    try:
        activity = MaintenanceActivity.objects.get(id=activity_id)
    except MaintenanceActivity.DoesNotExist:
        return Response(
            {'error': 'Atividade não encontrada.'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Verifica permissão
    if not (request.user == activity.technician or request.user.is_supervisor):
        return Response(
            {'error': 'Você não tem permissão para finalizar esta atividade.'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if activity.status != 'in_progress':
        return Response(
            {'error': f'Atividade não pode ser finalizada. Status atual: {activity.get_status_display()}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = ActivityCompleteSerializer(data=request.data)
    if serializer.is_valid():
        # Finaliza a atividade
        activity.status = 'completed'
        activity.completed_at = timezone.now()
        
        # Calcula duração real
        if activity.started_at:
            activity.actual_duration = activity.completed_at - activity.started_at
        
        if serializer.validated_data.get('observations'):
            activity.observations = serializer.validated_data['observations']
        
        activity.save()
        
        # Salva respostas
        answers_data = serializer.validated_data.get('answers', [])
        for answer_data in answers_data:
            ActivityAnswer.objects.update_or_create(
                activity=activity,
                question_id=answer_data['question_id'],
                defaults={
                    'answer_text': answer_data.get('answer_text', ''),
                    'answer_number': answer_data.get('answer_number'),
                    'answer_boolean': answer_data.get('answer_boolean'),
                }
            )
        
        # Salva peças utilizadas
        parts_data = serializer.validated_data.get('parts_used', [])
        for part_data in parts_data:
            PartUsage.objects.create(
                activity=activity,
                part_id=part_data['part_id'],
                quantity_used=part_data['quantity_used'],
                unit_cost=part_data.get('unit_cost'),
                observations=part_data.get('observations', '')
            )
            
            # Atualiza estoque da peça
            from parts.models import Part
            try:
                part = Part.objects.get(id=part_data['part_id'])
                part.current_stock -= part_data['quantity_used']
                part.save()
            except Part.DoesNotExist:
                pass
        
        return Response({
            'success': True,
            'message': 'Atividade finalizada com sucesso.',
            'activity': MaintenanceActivitySerializer(activity, context={'request': request}).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_photo(request, activity_id):
    """
    Upload de foto para uma atividade
    """
    try:
        activity = MaintenanceActivity.objects.get(id=activity_id)
    except MaintenanceActivity.DoesNotExist:
        return Response(
            {'error': 'Atividade não encontrada.'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Verifica permissão
    if not (request.user == activity.technician or request.user.is_supervisor):
        return Response(
            {'error': 'Você não tem permissão para adicionar fotos a esta atividade.'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = PhotoUploadSerializer(data=request.data)
    if serializer.is_valid():
        photo = serializer.save(activity=activity)
        
        return Response({
            'success': True,
            'message': 'Foto enviada com sucesso.',
            'photo': ActivityPhotoSerializer(photo, context={'request': request}).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def activity_stats(request):
    """
    Estatísticas de atividades
    """
    user = request.user
    
    # Filtros base
    queryset = MaintenanceActivity.objects.all()
    if not (user.is_supervisor or user.is_staff):
        queryset = queryset.filter(technician=user)
    
    # Contadores por status
    stats = {
        'total': queryset.count(),
        'pending': queryset.filter(status='pending').count(),
        'in_progress': queryset.filter(status='in_progress').count(),
        'completed': queryset.filter(status='completed').count(),
        'cancelled': queryset.filter(status='cancelled').count(),
    }
    
    # Estatísticas do mês atual
    current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_stats = {
        'created_this_month': queryset.filter(created_at__gte=current_month).count(),
        'completed_this_month': queryset.filter(
            status='completed',
            completed_at__gte=current_month
        ).count(),
    }
    
    # Atividades por prioridade
    priority_stats = dict(
        queryset.values('priority').annotate(count=Count('id')).values_list('priority', 'count')
    )
    
    return Response({
        'general': stats,
        'monthly': monthly_stats,
        'by_priority': priority_stats,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_activities(request):
    """
    Atividades do usuário logado
    """
    user = request.user
    
    activities = MaintenanceActivity.objects.filter(technician=user).order_by('-created_at')
    
    # Filtros opcionais
    status_filter = request.GET.get('status')
    if status_filter:
        activities = activities.filter(status=status_filter)
    
    serializer = MaintenanceActivityListSerializer(activities[:20], many=True)
    return Response({
        'activities': serializer.data,
        'total': activities.count()
    })

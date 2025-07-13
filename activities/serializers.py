from rest_framework import serializers
from .models import (
    ActivityType, StandardQuestion, MaintenanceActivity,
    PartUsage, ActivityPhoto, ActivityAnswer
)
from parts.serializers import PartListSerializer
from locations.serializers import LocationListSerializer
from authentication.serializers import UserProfileSerializer


class StandardQuestionSerializer(serializers.ModelSerializer):
    """
    Serializer para perguntas padrão
    """
    question_type_display = serializers.CharField(source='get_question_type_display', read_only=True)
    
    class Meta:
        model = StandardQuestion
        fields = [
            'id', 'question', 'question_type', 'question_type_display',
            'choices', 'is_required', 'order'
        ]


class ActivityTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para tipos de atividade
    """
    questions = StandardQuestionSerializer(many=True, read_only=True)
    activities_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ActivityType
        fields = [
            'id', 'name', 'description', 'estimated_time', 'requires_parts',
            'is_active', 'questions', 'activities_count', 'created_at'
        ]
    
    def get_activities_count(self, obj):
        return obj.maintenanceactivity_set.count()


class ActivityPhotoSerializer(serializers.ModelSerializer):
    """
    Serializer para fotos das atividades
    """
    photo_type_display = serializers.CharField(source='get_photo_type_display', read_only=True)
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ActivityPhoto
        fields = [
            'id', 'photo', 'photo_url', 'photo_type', 'photo_type_display',
            'description', 'taken_at'
        ]
    
    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
        return None


class PartUsageSerializer(serializers.ModelSerializer):
    """
    Serializer para uso de peças
    """
    part_details = PartListSerializer(source='part', read_only=True)
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = PartUsage
        fields = [
            'id', 'part', 'part_details', 'quantity_used', 'unit_cost',
            'total_cost', 'observations', 'created_at'
        ]


class ActivityAnswerSerializer(serializers.ModelSerializer):
    """
    Serializer para respostas das atividades
    """
    question_details = StandardQuestionSerializer(source='question', read_only=True)
    
    class Meta:
        model = ActivityAnswer
        fields = [
            'id', 'question', 'question_details', 'answer_text',
            'answer_number', 'answer_boolean', 'created_at'
        ]


class MaintenanceActivitySerializer(serializers.ModelSerializer):
    """
    Serializer completo para atividades de manutenção
    """
    technician_details = UserProfileSerializer(source='technician', read_only=True)
    activity_type_details = ActivityTypeSerializer(source='activity_type', read_only=True)
    location_details = LocationListSerializer(source='location', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    # Campos relacionados
    parts_used = PartUsageSerializer(many=True, read_only=True)
    photos = ActivityPhotoSerializer(many=True, read_only=True)
    answers = ActivityAnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = MaintenanceActivity
        fields = [
            'id', 'technician', 'technician_details', 'activity_type', 'activity_type_details',
            'location', 'location_details', 'title', 'description', 'status', 'status_display',
            'priority', 'priority_display', 'scheduled_date', 'started_at', 'completed_at',
            'estimated_duration', 'actual_duration', 'observations', 'parts_used', 'photos',
            'answers', 'created_at', 'updated_at'
        ]


class MaintenanceActivityListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listagem
    """
    technician_name = serializers.CharField(source='technician.get_full_name', read_only=True)
    activity_type_name = serializers.CharField(source='activity_type.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = MaintenanceActivity
        fields = [
            'id', 'title', 'technician_name', 'activity_type_name', 'location_name',
            'status', 'status_display', 'priority', 'priority_display',
            'scheduled_date', 'created_at'
        ]


class MaintenanceActivityCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de atividades
    """
    class Meta:
        model = MaintenanceActivity
        fields = [
            'activity_type', 'location', 'title', 'description',
            'priority', 'scheduled_date', 'estimated_duration'
        ]
    
    def create(self, validated_data):
        # Define o técnico como o usuário logado
        validated_data['technician'] = self.context['request'].user
        return super().create(validated_data)


class ActivityStartSerializer(serializers.Serializer):
    """
    Serializer para iniciar uma atividade
    """
    observations = serializers.CharField(required=False, allow_blank=True)


class ActivityCompleteSerializer(serializers.Serializer):
    """
    Serializer para finalizar uma atividade
    """
    observations = serializers.CharField(required=False, allow_blank=True)
    answers = serializers.ListField(
        child=serializers.DictField(),
        required=False
    )
    parts_used = serializers.ListField(
        child=serializers.DictField(),
        required=False
    )
    
    def validate_answers(self, value):
        """Valida as respostas às perguntas padrão"""
        for answer in value:
            if 'question_id' not in answer:
                raise serializers.ValidationError("question_id é obrigatório para cada resposta.")
        return value
    
    def validate_parts_used(self, value):
        """Valida as peças utilizadas"""
        for part_usage in value:
            if 'part_id' not in part_usage or 'quantity_used' not in part_usage:
                raise serializers.ValidationError(
                    "part_id e quantity_used são obrigatórios para cada peça."
                )
        return value


class PhotoUploadSerializer(serializers.ModelSerializer):
    """
    Serializer para upload de fotos
    """
    class Meta:
        model = ActivityPhoto
        fields = ['photo', 'photo_type', 'description']

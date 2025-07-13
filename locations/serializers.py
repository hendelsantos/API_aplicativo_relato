from rest_framework import serializers
from .models import Location


class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer para locais
    """
    location_type_display = serializers.CharField(source='get_location_type_display', read_only=True)
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    full_path = serializers.CharField(read_only=True)
    level = serializers.IntegerField(read_only=True)
    children_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Location
        fields = [
            'id', 'name', 'code', 'location_type', 'location_type_display',
            'parent', 'parent_name', 'description', 'full_path', 'level',
            'children_count', 'is_active', 'created_at', 'updated_at'
        ]
    
    def get_children_count(self, obj):
        return obj.children.filter(is_active=True).count()


class LocationTreeSerializer(serializers.ModelSerializer):
    """
    Serializer para árvore de locais (com filhos)
    """
    children = serializers.SerializerMethodField()
    location_type_display = serializers.CharField(source='get_location_type_display', read_only=True)
    
    class Meta:
        model = Location
        fields = [
            'id', 'name', 'code', 'location_type', 'location_type_display',
            'description', 'is_active', 'children'
        ]
    
    def get_children(self, obj):
        children = obj.children.filter(is_active=True).order_by('name')
        return LocationTreeSerializer(children, many=True).data


class LocationListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listagem
    """
    full_path = serializers.CharField(read_only=True)
    location_type_display = serializers.CharField(source='get_location_type_display', read_only=True)
    
    class Meta:
        model = Location
        fields = [
            'id', 'name', 'code', 'location_type', 'location_type_display',
            'full_path', 'is_active'
        ]


class LocationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de locais
    """
    class Meta:
        model = Location
        fields = [
            'name', 'code', 'location_type', 'parent', 'description'
        ]
    
    def validate(self, attrs):
        # Validações específicas de negócio
        parent = attrs.get('parent')
        location_type = attrs.get('location_type')
        
        if parent:
            # Verifica hierarquia lógica
            if parent.location_type == 'component' and location_type != 'component':
                raise serializers.ValidationError(
                    "Componentes só podem ter outros componentes como filhos."
                )
            
            # Evita referência circular
            if parent.parent and parent.parent == attrs.get('parent'):
                raise serializers.ValidationError(
                    "Não é possível criar referência circular."
                )
        
        return attrs

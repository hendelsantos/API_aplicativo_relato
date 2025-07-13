from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Location
from .serializers import (
    LocationSerializer,
    LocationTreeSerializer,
    LocationListSerializer,
    LocationCreateSerializer
)


class LocationListCreateView(generics.ListCreateAPIView):
    """
    Lista e cria locais
    """
    queryset = Location.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'location_type', 'created_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LocationCreateSerializer
        return LocationListSerializer


class LocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalhe, atualiza e deleta local
    """
    queryset = Location.objects.filter(is_active=True)
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_destroy(self, instance):
        # Soft delete
        instance.is_active = False
        instance.save()
        
        # Desativa também todos os filhos
        descendants = instance.get_descendants()
        for descendant in descendants:
            descendant.is_active = False
            descendant.save()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def location_tree(request):
    """
    Retorna a árvore completa de locais
    """
    # Pega apenas os locais raiz (sem parent)
    root_locations = Location.objects.filter(
        parent__isnull=True, 
        is_active=True
    ).order_by('name')
    
    serializer = LocationTreeSerializer(root_locations, many=True)
    return Response({
        'tree': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def location_children(request, location_id):
    """
    Retorna os filhos de um local específico
    """
    try:
        location = Location.objects.get(id=location_id, is_active=True)
    except Location.DoesNotExist:
        return Response(
            {'error': 'Local não encontrado.'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    children = location.children.filter(is_active=True).order_by('name')
    serializer = LocationListSerializer(children, many=True)
    
    return Response({
        'parent': LocationSerializer(location).data,
        'children': serializer.data,
        'count': children.count()
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def location_path(request, location_id):
    """
    Retorna o caminho completo até um local
    """
    try:
        location = Location.objects.get(id=location_id, is_active=True)
    except Location.DoesNotExist:
        return Response(
            {'error': 'Local não encontrado.'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Monta o caminho completo
    path = [location]
    path.extend(location.get_ancestors())
    path.reverse()  # Do raiz para o atual
    
    serializer = LocationListSerializer(path, many=True)
    return Response({
        'path': serializer.data,
        'current_location': LocationSerializer(location).data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def locations_by_type(request, location_type):
    """
    Lista locais por tipo
    """
    valid_types = [choice[0] for choice in Location.LOCATION_TYPES]
    
    if location_type not in valid_types:
        return Response(
            {'error': f'Tipo inválido. Tipos válidos: {valid_types}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    locations = Location.objects.filter(
        location_type=location_type, 
        is_active=True
    ).order_by('name')
    
    serializer = LocationListSerializer(locations, many=True)
    return Response({
        'type': location_type,
        'count': locations.count(),
        'locations': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def location_search(request):
    """
    Busca avançada de locais
    """
    query = request.GET.get('q', '')
    location_type = request.GET.get('type', '')
    parent_id = request.GET.get('parent', '')
    
    locations = Location.objects.filter(is_active=True)
    
    if query:
        locations = locations.filter(
            Q(name__icontains=query) |
            Q(code__icontains=query) |
            Q(description__icontains=query)
        )
    
    if location_type:
        locations = locations.filter(location_type=location_type)
    
    if parent_id:
        locations = locations.filter(parent_id=parent_id)
    
    serializer = LocationListSerializer(locations[:50], many=True)  # Limita a 50 resultados
    return Response({
        'query': query,
        'count': locations.count(),
        'locations': serializer.data
    })

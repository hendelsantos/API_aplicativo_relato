from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from .models import User
from .serializers import (
    UserSerializer, 
    UserProfileSerializer, 
    ChangePasswordSerializer
)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View para ver e atualizar perfil do usuário logado
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    """
    Lista todos os técnicos (apenas para supervisores)
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_supervisor or user.is_staff:
            return User.objects.filter(is_active=True)
        else:
            # Técnicos só veem próprio perfil
            return User.objects.filter(id=user.id)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Endpoint para mudança de senha
    """
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        
        # Verifica senha atual
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'error': 'Senha atual incorreta.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Define nova senha
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Atualiza a sessão para evitar logout
        update_session_auth_hash(request, user)
        
        return Response(
            {'message': 'Senha alterada com sucesso.'}, 
            status=status.HTTP_200_OK
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats(request):
    """
    Estatísticas do usuário logado
    """
    user = request.user
    
    # Importação aqui para evitar dependência circular
    from activities.models import MaintenanceActivity
    
    activities_count = MaintenanceActivity.objects.filter(technician=user).count()
    completed_activities = MaintenanceActivity.objects.filter(
        technician=user, 
        status='completed'
    ).count()
    pending_activities = MaintenanceActivity.objects.filter(
        technician=user, 
        status='pending'
    ).count()
    
    return Response({
        'user': UserProfileSerializer(user).data,
        'stats': {
            'total_activities': activities_count,
            'completed_activities': completed_activities,
            'pending_activities': pending_activities,
        }
    })

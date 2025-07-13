from django.urls import path
from . import views

urlpatterns = [
    # Tipos de atividade
    path('types/', views.ActivityTypeListView.as_view(), name='activity-type-list'),
    
    # CRUD de atividades
    path('', views.MaintenanceActivityListCreateView.as_view(), name='activity-list'),
    path('<int:pk>/', views.MaintenanceActivityDetailView.as_view(), name='activity-detail'),
    
    # Ações em atividades
    path('<int:activity_id>/start/', views.start_activity, name='start-activity'),
    path('<int:activity_id>/complete/', views.complete_activity, name='complete-activity'),
    path('<int:activity_id>/upload-photo/', views.upload_photo, name='upload-photo'),
    
    # Estatísticas e relatórios
    path('stats/', views.activity_stats, name='activity-stats'),
    path('my-activities/', views.my_activities, name='my-activities'),
]

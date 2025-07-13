from django.urls import path
from . import views

urlpatterns = [
    # CRUD básico
    path('', views.LocationListCreateView.as_view(), name='location-list'),
    path('<int:pk>/', views.LocationDetailView.as_view(), name='location-detail'),
    
    # Funcionalidades especiais
    path('tree/', views.location_tree, name='location-tree'),
    path('<int:location_id>/children/', views.location_children, name='location-children'),
    path('<int:location_id>/path/', views.location_path, name='location-path'),
    path('type/<str:location_type>/', views.locations_by_type, name='locations-by-type'),
    path('search/', views.location_search, name='location-search'),
]

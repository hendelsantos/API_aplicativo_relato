from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('change-password/', views.change_password, name='change-password'),
    path('stats/', views.user_stats, name='user-stats'),
]

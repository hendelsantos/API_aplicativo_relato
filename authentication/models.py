from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modelo customizado de usuário para técnicos de manutenção
    """
    SHIFT_CHOICES = [
        ('morning', 'Manhã (6h-14h)'),
        ('afternoon', 'Tarde (14h-22h)'),
        ('night', 'Noite (22h-6h)'),
    ]
    
    employee_id = models.CharField(max_length=20, unique=True, verbose_name="ID do Funcionário")
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES, verbose_name="Turno")
    phone = models.CharField(max_length=15, blank=True, verbose_name="Telefone")
    is_supervisor = models.BooleanField(default=False, verbose_name="É Supervisor")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Técnico"
        verbose_name_plural = "Técnicos"
        
    def __str__(self):
        return f"{self.get_full_name()} - {self.employee_id} ({self.get_shift_display()})"

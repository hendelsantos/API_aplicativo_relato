from django.db import models
from django.conf import settings
from parts.models import Part
from locations.models import Location


class ActivityType(models.Model):
    """
    Tipo de atividade de manutenção
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome da Atividade")
    description = models.TextField(blank=True, verbose_name="Descrição")
    estimated_time = models.DurationField(null=True, blank=True, verbose_name="Tempo Estimado")
    requires_parts = models.BooleanField(default=True, verbose_name="Requer Peças")
    is_active = models.BooleanField(default=True, verbose_name="Ativa")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Tipo de Atividade"
        verbose_name_plural = "Tipos de Atividades"
        
    def __str__(self):
        return self.name


class StandardQuestion(models.Model):
    """
    Perguntas padrão para cada tipo de atividade
    """
    QUESTION_TYPES = [
        ('yes_no', 'Sim/Não'),
        ('text', 'Texto'),
        ('number', 'Número'),
        ('multiple_choice', 'Múltipla Escolha'),
    ]
    
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField(verbose_name="Pergunta")
    question_type = models.CharField(max_length=15, choices=QUESTION_TYPES, verbose_name="Tipo da Pergunta")
    choices = models.JSONField(blank=True, null=True, verbose_name="Opções (para múltipla escolha)")
    is_required = models.BooleanField(default=True, verbose_name="Obrigatória")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem")
    
    class Meta:
        verbose_name = "Pergunta Padrão"
        verbose_name_plural = "Perguntas Padrão"
        ordering = ['activity_type', 'order']
        
    def __str__(self):
        return f"{self.activity_type.name} - {self.question[:50]}"


class MaintenanceActivity(models.Model):
    """
    Atividade de manutenção executada
    """
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('in_progress', 'Em Andamento'),
        ('completed', 'Concluída'),
        ('cancelled', 'Cancelada'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Baixa'),
        ('medium', 'Média'),
        ('high', 'Alta'),
        ('critical', 'Crítica'),
    ]
    
    technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Técnico")
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE, verbose_name="Tipo de Atividade")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Local")
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name="Prioridade")
    scheduled_date = models.DateTimeField(null=True, blank=True, verbose_name="Data Agendada")
    started_at = models.DateTimeField(null=True, blank=True, verbose_name="Iniciado em")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Concluído em")
    estimated_duration = models.DurationField(null=True, blank=True, verbose_name="Duração Estimada")
    actual_duration = models.DurationField(null=True, blank=True, verbose_name="Duração Real")
    observations = models.TextField(blank=True, verbose_name="Observações")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Atividade de Manutenção"
        verbose_name_plural = "Atividades de Manutenção"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} - {self.location.name} ({self.get_status_display()})"


class PartUsage(models.Model):
    """
    Peças utilizadas em uma atividade
    """
    activity = models.ForeignKey(MaintenanceActivity, on_delete=models.CASCADE, related_name='parts_used')
    part = models.ForeignKey(Part, on_delete=models.CASCADE, verbose_name="Peça")
    quantity_used = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantidade Utilizada")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Custo Unitário")
    observations = models.TextField(blank=True, verbose_name="Observações")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Uso de Peça"
        verbose_name_plural = "Uso de Peças"
        unique_together = ['activity', 'part']
        
    def __str__(self):
        return f"{self.part.name} - {self.quantity_used} {self.part.unit}"
    
    @property
    def total_cost(self):
        """Calcula o custo total da peça utilizada"""
        if self.unit_cost:
            return self.quantity_used * self.unit_cost
        return None


class ActivityPhoto(models.Model):
    """
    Fotos anexadas à atividade de manutenção
    """
    PHOTO_TYPES = [
        ('before', 'Antes'),
        ('during', 'Durante'),
        ('after', 'Depois'),
        ('problem', 'Problema'),
        ('solution', 'Solução'),
    ]
    
    activity = models.ForeignKey(MaintenanceActivity, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='activity_photos/', verbose_name="Foto")
    photo_type = models.CharField(max_length=10, choices=PHOTO_TYPES, verbose_name="Tipo da Foto")
    description = models.CharField(max_length=200, blank=True, verbose_name="Descrição")
    taken_at = models.DateTimeField(auto_now_add=True, verbose_name="Tirada em")
    
    class Meta:
        verbose_name = "Foto da Atividade"
        verbose_name_plural = "Fotos das Atividades"
        ordering = ['taken_at']
        
    def __str__(self):
        return f"{self.activity.title} - {self.get_photo_type_display()}"


class ActivityAnswer(models.Model):
    """
    Respostas às perguntas padrão da atividade
    """
    activity = models.ForeignKey(MaintenanceActivity, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(StandardQuestion, on_delete=models.CASCADE, verbose_name="Pergunta")
    answer_text = models.TextField(blank=True, verbose_name="Resposta Texto")
    answer_number = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Resposta Número")
    answer_boolean = models.BooleanField(null=True, blank=True, verbose_name="Resposta Sim/Não")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Resposta da Atividade"
        verbose_name_plural = "Respostas das Atividades"
        unique_together = ['activity', 'question']
        
    def __str__(self):
        return f"{self.activity.title} - {self.question.question[:30]}"

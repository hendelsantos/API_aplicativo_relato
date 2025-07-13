from django.db import models


class Location(models.Model):
    """
    Modelo para estrutura hierárquica de locais
    Ex: Fábrica > Setor > Equipamento > Componente
    """
    LOCATION_TYPES = [
        ('plant', 'Planta/Fábrica'),
        ('sector', 'Setor'),
        ('line', 'Linha de Produção'),
        ('equipment', 'Equipamento'),
        ('component', 'Componente'),
        ('area', 'Área'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Nome do Local")
    code = models.CharField(max_length=50, unique=True, verbose_name="Código do Local")
    location_type = models.CharField(max_length=10, choices=LOCATION_TYPES, verbose_name="Tipo de Local")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='children', verbose_name="Local Pai")
    description = models.TextField(blank=True, verbose_name="Descrição")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Local"
        verbose_name_plural = "Locais"
        ordering = ['parent', 'name']
        
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @property
    def full_path(self):
        """Retorna o caminho completo do local"""
        path = [self.name]
        parent = self.parent
        while parent:
            path.insert(0, parent.name)
            parent = parent.parent
        return " > ".join(path)
    
    @property
    def level(self):
        """Retorna o nível hierárquico do local"""
        level = 0
        parent = self.parent
        while parent:
            level += 1
            parent = parent.parent
        return level
    
    def get_descendants(self):
        """Retorna todos os descendentes do local"""
        descendants = []
        for child in self.children.all():
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants
    
    def get_ancestors(self):
        """Retorna todos os ancestrais do local"""
        ancestors = []
        parent = self.parent
        while parent:
            ancestors.append(parent)
            parent = parent.parent
        return ancestors

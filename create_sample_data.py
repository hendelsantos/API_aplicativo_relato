"""
Script para criar dados de exemplo para demonstração
"""

from authentication.models import User
from parts.models import PartCategory, Part
from locations.models import Location
from activities.models import ActivityType, StandardQuestion, MaintenanceActivity

# Criar técnicos
tecnico1 = User.objects.create_user(
    username='joao.silva',
    email='joao@empresa.com',
    password='tecnico123',
    first_name='João',
    last_name='Silva',
    employee_id='TEC001',
    shift='morning'
)

tecnico2 = User.objects.create_user(
    username='maria.santos',
    email='maria@empresa.com',
    password='tecnico123',
    first_name='Maria',
    last_name='Santos',
    employee_id='TEC002',
    shift='afternoon',
    is_supervisor=True
)

# Criar categorias de peças
cat_rolamentos = PartCategory.objects.create(
    name='Rolamentos',
    description='Rolamentos diversos para equipamentos'
)

cat_correias = PartCategory.objects.create(
    name='Correias',
    description='Correias e polias'
)

cat_filtros = PartCategory.objects.create(
    name='Filtros',
    description='Filtros de óleo, ar e combustível'
)

# Criar peças
Part.objects.create(
    code='ROL001',
    name='Rolamento 6205',
    category=cat_rolamentos,
    description='Rolamento de esfera 6205',
    minimum_stock=10,
    current_stock=25,
    cost_price=45.50,
    supplier='Rolamentos Brasil'
)

Part.objects.create(
    code='COR001',
    name='Correia V A42',
    category=cat_correias,
    description='Correia em V perfil A42',
    minimum_stock=5,
    current_stock=3,  # Estoque baixo
    cost_price=28.90,
    supplier='Correias SP'
)

Part.objects.create(
    code='FIL001',
    name='Filtro de Óleo W67',
    category=cat_filtros,
    description='Filtro de óleo para motores',
    minimum_stock=20,
    current_stock=50,
    cost_price=15.30,
    supplier='Filtros ABC'
)

# Criar estrutura de locais
fabrica = Location.objects.create(
    name='Fábrica Principal',
    code='FAB001',
    location_type='plant',
    description='Fábrica principal da empresa'
)

setor_producao = Location.objects.create(
    name='Setor de Produção',
    code='PROD001',
    location_type='sector',
    parent=fabrica,
    description='Setor de produção principal'
)

linha1 = Location.objects.create(
    name='Linha de Produção 1',
    code='LIN001',
    location_type='line',
    parent=setor_producao,
    description='Primeira linha de produção'
)

equipamento1 = Location.objects.create(
    name='Compressor Atlas 01',
    code='COMP001',
    location_type='equipment',
    parent=linha1,
    description='Compressor principal da linha 1'
)

# Criar tipos de atividade
manutencao_preventiva = ActivityType.objects.create(
    name='Manutenção Preventiva',
    description='Manutenção preventiva programada',
    requires_parts=True
)

manutencao_corretiva = ActivityType.objects.create(
    name='Manutenção Corretiva',
    description='Manutenção corretiva não programada',
    requires_parts=True
)

# Criar perguntas padrão
StandardQuestion.objects.create(
    activity_type=manutencao_preventiva,
    question='O equipamento estava funcionando normalmente antes da manutenção?',
    question_type='yes_no',
    order=1
)

StandardQuestion.objects.create(
    activity_type=manutencao_preventiva,
    question='Qual a temperatura do motor em °C?',
    question_type='number',
    order=2
)

StandardQuestion.objects.create(
    activity_type=manutencao_corretiva,
    question='Qual foi o problema identificado?',
    question_type='text',
    order=1
)

# Criar atividade de exemplo
MaintenanceActivity.objects.create(
    technician=tecnico1,
    activity_type=manutencao_preventiva,
    location=equipamento1,
    title='Manutenção Preventiva - Compressor Atlas 01',
    description='Manutenção preventiva mensal do compressor',
    priority='medium',
    status='pending'
)

print("Dados de exemplo criados com sucesso!")
print("\nUsuários criados:")
print("- admin / admin123 (superusuário)")
print("- joao.silva / tecnico123 (técnico)")
print("- maria.santos / tecnico123 (supervisora)")
print("\nAcesse: http://localhost:8000/admin/")

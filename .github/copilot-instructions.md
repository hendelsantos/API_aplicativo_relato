<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Sistema de Relatório de Manutenção - Instruções para Copilot

Este é um projeto Django REST API para sistema de manutenção industrial com aplicativo Flutter.

## Contexto do Projeto

### Problema a ser resolvido:
- Equipe de manutenção com 3 turnos relatava peças e atividades via WhatsApp
- Sistema falho causava esquecimentos e furos de estoque
- Falta de padronização e rastreabilidade

### Solução implementada:
- API Django com autenticação JWT
- QR codes para identificação de peças
- Estrutura hierárquica de locais
- Formulários padronizados de atividades
- Upload de fotos e controle de estoque

## Estrutura do Projeto

- `authentication/` - Gestão de usuários e técnicos (3 turnos)
- `parts/` - Peças, categorias, QR codes e estoque
- `locations/` - Estrutura hierárquica de locais (árvore)
- `activities/` - Atividades de manutenção, fotos, respostas

## Diretrizes de Código

### Django/Python:
- Use Django REST Framework para todas as APIs
- Implemente validações robustas nos serializers
- Mantenha separação clara entre models, serializers e views
- Use permissions apropriadas (IsAuthenticated, custom permissions)
- Implemente soft delete quando necessário

### Modelos:
- Use verbose_name em português para admin
- Implemente __str__ methods descritivos
- Use choices para campos com opções limitadas
- Adicione timestamps (created_at, updated_at)

### APIs:
- Retorne dados estruturados com success/error
- Use status codes HTTP apropriados
- Implemente paginação quando necessário
- Adicione filtros e busca em list views

### Segurança:
- Valide permissões em todas as views
- Use JWT para autenticação
- Implemente rate limiting em produção
- Validação rigorosa de uploads

### Funcionalidades Específicas:
- QR codes são gerados automaticamente para peças
- Estoque é atualizado automaticamente ao usar peças
- Hierarquia de locais deve ser respeitada
- Fotos são organizadas por tipo (antes/durante/depois)

## Padrões de Nomenclatura

- Models: CamelCase (ex: MaintenanceActivity)
- Views: snake_case com sufixos View/ViewSet
- URLs: kebab-case (ex: /update-stock/)
- Campos: snake_case

## Próximas Implementações

1. Relatórios automáticos por email
2. Dashboard web para supervisores
3. Notificações push para o app móvel
4. Integração com sistemas ERP
5. Backup automático e logs de auditoria

Mantenha o foco na robustez, usabilidade e rastreabilidade do sistema.

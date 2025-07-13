# Contribuindo para o Sistema de Manutenção

Obrigado por seu interesse em contribuir para este projeto! Este guia contém informações sobre como contribuir efetivamente.

## 🚀 Como Contribuir

### 1. Fork do Projeto
```bash
# Clone seu fork
git clone https://github.com/seu-usuario/API_aplicativo_relato.git
cd API_aplicativo_relato
```

### 2. Configuração do Ambiente

#### Backend (Django)
```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Edite o .env com suas configurações

# Executar migrações
python manage.py migrate

# Criar dados de exemplo (opcional)
python create_sample_data.py

# Executar servidor
python manage.py runserver
```

#### Frontend (Flutter)
```bash
cd flutter_app

# Instalar dependências
flutter pub get

# Executar em modo debug
flutter run
```

### 3. Desenvolvimento

#### Estrutura do Projeto
- `authentication/` - Gestão de usuários e autenticação JWT
- `parts/` - Peças, categorias, QR codes e estoque
- `locations/` - Estrutura hierárquica de locais
- `activities/` - Atividades de manutenção e relatórios
- `flutter_app/` - Aplicativo móvel Flutter

#### Padrões de Código

##### Django/Python
- Siga PEP 8 para formatação
- Use type hints quando possível
- Docstrings em português para funções públicas
- Validações robustas nos serializers
- Testes unitários para novas funcionalidades

##### Flutter/Dart
- Siga as convenções do Dart
- Use Provider para gerenciamento de estado
- Componentes reutilizáveis na pasta `widgets/`
- Tratamento de erros consistente

#### Commits
```bash
# Formato recomendado
git commit -m "feat: adicionar validação de estoque negativo"
git commit -m "fix: corrigir bug no upload de fotos"
git commit -m "docs: atualizar README com novas funcionalidades"
```

Tipos de commit:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (sem mudança de código)
- `refactor`: Refatoração de código
- `test`: Adicionar ou corrigir testes
- `chore`: Tarefas de manutenção

### 4. Pull Requests

#### Antes de Submeter
- [ ] Código testado localmente
- [ ] Testes passando
- [ ] Documentação atualizada
- [ ] Sem conflitos com a branch main

#### Template de PR
```markdown
## Descrição
Breve descrição das mudanças implementadas.

## Tipo de Mudança
- [ ] Bug fix
- [ ] Nova funcionalidade
- [ ] Breaking change
- [ ] Documentação

## Como Testar
1. Passos para reproduzir/testar
2. Dados de teste necessários
3. Comportamento esperado

## Screenshots (se aplicável)
Adicione capturas de tela se houver mudanças na UI.

## Checklist
- [ ] Meu código segue os padrões do projeto
- [ ] Revisei meu próprio código
- [ ] Comentei partes complexas do código
- [ ] Atualizei a documentação
- [ ] Meus testes passam localmente
```

## 🐛 Reportando Bugs

Use o template de issue para reportar bugs:

```markdown
**Descrição do Bug**
Descrição clara e concisa do bug.

**Para Reproduzir**
Passos para reproduzir o comportamento:
1. Vá para '...'
2. Clique em '....'
3. Role para baixo até '....'
4. Veja o erro

**Comportamento Esperado**
O que você esperava que acontecesse.

**Screenshots**
Se aplicável, adicione screenshots.

**Ambiente:**
 - OS: [e.g. Android, iOS]
 - Versão do App: [e.g. 1.0.0]
 - Dispositivo: [e.g. Samsung Galaxy S21]

**Informações Adicionais**
Qualquer outra informação sobre o problema.
```

## 💡 Sugerindo Funcionalidades

Para sugerir novas funcionalidades:

1. Verifique se não existe issue similar
2. Use o template de feature request
3. Descreva o problema que a funcionalidade resolve
4. Explique a solução proposta
5. Considere alternativas

## 📋 Roadmap de Funcionalidades

### Próximas Implementações
1. **Relatórios Automáticos**
   - Envio por email
   - Agendamento personalizado
   - Múltiplos formatos (PDF, Excel)

2. **Dashboard Web**
   - Interface para supervisores
   - Gráficos de produtividade
   - Controle de estoque avançado

3. **Notificações Push**
   - Lembretes de manutenção
   - Alertas de estoque baixo
   - Notificações de atividades urgentes

4. **Integração ERP**
   - Sincronização de peças
   - Controle de custos
   - Relatórios financeiros

5. **Melhorias de Performance**
   - Cache de dados
   - Otimização de queries
   - Compressão de imagens

## 🤝 Comunidade

- Seja respeitoso e construtivo
- Ajude outros desenvolvedores
- Documente suas contribuições
- Teste thoroughly suas mudanças

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença do projeto.

---

**Dúvidas?** Abra uma issue com a tag `question` ou entre em contato com os mantenedores.

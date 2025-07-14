"""
Comando Django para restaurar backup do sistema
"""
import os
import json
from django.core.management.base import BaseCommand
from django.core import serializers
from django.db import transaction
from django.apps import apps


class Command(BaseCommand):
    help = 'Restaurar backup do sistema de manutenção'

    def add_arguments(self, parser):
        parser.add_argument(
            'backup_file',
            type=str,
            help='Caminho para o arquivo de backup'
        )
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirmar restauração (CUIDADO: sobrescreve dados existentes)'
        )

    def handle(self, *args, **options):
        backup_file = options['backup_file']
        
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    '⚠️  ATENÇÃO: Esta operação irá SOBRESCREVER todos os dados existentes!'
                )
            )
            self.stdout.write('Para confirmar, execute novamente com --confirm')
            return
        
        if not os.path.exists(backup_file):
            self.stdout.write(
                self.style.ERROR(f'❌ Arquivo de backup não encontrado: {backup_file}')
            )
            return
        
        self.stdout.write('🔄 Iniciando restauração do backup...')
        self.stdout.write(f'📁 Arquivo: {backup_file}')
        
        try:
            # Carregar backup
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            # Verificar formato do backup
            if 'metadata' not in backup_data or 'data' not in backup_data:
                self.stdout.write(
                    self.style.ERROR('❌ Formato de backup inválido')
                )
                return
            
            metadata = backup_data['metadata']
            self.stdout.write(f'📊 Backup criado em: {metadata["created_at"]}')
            self.stdout.write(f'🔖 Versão: {metadata["version"]}')
            
            # Restaurar dados dentro de uma transação
            with transaction.atomic():
                for app_name, app_data in backup_data['data'].items():
                    self.stdout.write(f'📦 Restaurando app: {app_name}')
                    
                    # Obter app config
                    try:
                        app_config = apps.get_app_config(app_name)
                    except LookupError:
                        self.stdout.write(
                            self.style.WARNING(f'⚠️  App {app_name} não encontrada, pulando...')
                        )
                        continue
                    
                    for model_name, model_data in app_data.items():
                        self.stdout.write(f'  📋 Restaurando modelo: {model_name}')
                        
                        # Obter modelo
                        try:
                            model = app_config.get_model(model_name)
                        except LookupError:
                            self.stdout.write(
                                self.style.WARNING(f'    ⚠️  Modelo {model_name} não encontrado, pulando...')
                            )
                            continue
                        
                        # Limpar dados existentes
                        deleted_count = model.objects.count()
                        model.objects.all().delete()
                        self.stdout.write(f'    🗑️  {deleted_count} registros existentes removidos')
                        
                        # Restaurar dados
                        if isinstance(model_data, list) and model_data:
                            # Converter de volta para JSON se necessário
                            json_data = json.dumps(model_data)
                            
                            # Deserializar objetos
                            objects = []
                            for deserialized_obj in serializers.deserialize('json', json_data):
                                objects.append(deserialized_obj.object)
                            
                            # Salvar em lote
                            model.objects.bulk_create(objects)
                            self.stdout.write(f'    ✅ {len(objects)} registros restaurados')
                        else:
                            self.stdout.write(f'    ℹ️  Nenhum dado para restaurar')
            
            self.stdout.write('🎉 Restauração concluída com sucesso!')
            
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR('❌ Erro ao ler arquivo de backup: formato JSON inválido')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro durante a restauração: {str(e)}')
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS('✅ Sistema restaurado com sucesso!')
        )
        self.stdout.write('🔄 Considere reiniciar o servidor Django')

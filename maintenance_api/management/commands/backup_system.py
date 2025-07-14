"""
Comando Django para backup automático do banco de dados
"""
import os
import json
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core import serializers
from django.apps import apps


class Command(BaseCommand):
    help = 'Criar backup completo do sistema de manutenção'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            type=str,
            default='backups',
            help='Diretório para salvar o backup'
        )
        parser.add_argument(
            '--format',
            type=str,
            choices=['json', 'xml'],
            default='json',
            help='Formato do backup'
        )

    def handle(self, *args, **options):
        self.stdout.write('🔄 Iniciando backup do sistema...')
        
        # Criar diretório de backup
        backup_dir = options['output_dir']
        os.makedirs(backup_dir, exist_ok=True)
        
        # Nome do arquivo com timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'backup_sistema_manutencao_{timestamp}.{options["format"]}'
        backup_path = os.path.join(backup_dir, backup_filename)
        
        try:
            # Obter todos os modelos das apps locais
            local_apps = ['authentication', 'parts', 'locations', 'activities']
            
            backup_data = {
                'metadata': {
                    'created_at': datetime.datetime.now().isoformat(),
                    'version': '1.0.0',
                    'format': options['format'],
                    'apps': local_apps
                },
                'data': {}
            }
            
            for app_name in local_apps:
                self.stdout.write(f'📦 Fazendo backup da app: {app_name}')
                app_models = apps.get_app_config(app_name).get_models()
                backup_data['data'][app_name] = {}
                
                for model in app_models:
                    model_name = model._meta.model_name
                    self.stdout.write(f'  📋 Backup do modelo: {model_name}')
                    
                    # Serializar todos os objetos do modelo
                    queryset = model.objects.all()
                    serialized_data = serializers.serialize(options['format'], queryset)
                    
                    if options['format'] == 'json':
                        backup_data['data'][app_name][model_name] = json.loads(serialized_data)
                    else:
                        backup_data['data'][app_name][model_name] = serialized_data
                    
                    count = queryset.count()
                    self.stdout.write(f'    ✅ {count} registros copiados')
            
            # Salvar backup
            with open(backup_path, 'w', encoding='utf-8') as f:
                if options['format'] == 'json':
                    json.dump(backup_data, f, indent=2, ensure_ascii=False, default=str)
                else:
                    f.write(str(backup_data))
            
            # Estatísticas
            file_size = os.path.getsize(backup_path)
            file_size_mb = file_size / (1024 * 1024)
            
            self.stdout.write('🎉 Backup concluído com sucesso!')
            self.stdout.write(f'📁 Arquivo: {backup_path}')
            self.stdout.write(f'📊 Tamanho: {file_size_mb:.2f} MB')
            
            # Listar arquivos de backup existentes
            backup_files = [f for f in os.listdir(backup_dir) if f.startswith('backup_sistema_manutencao_')]
            backup_files.sort(reverse=True)
            
            self.stdout.write(f'📋 Total de backups: {len(backup_files)}')
            if len(backup_files) > 5:
                self.stdout.write('⚠️  Considere limpar backups antigos')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro durante o backup: {str(e)}')
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS('✅ Backup finalizado com sucesso!')
        )

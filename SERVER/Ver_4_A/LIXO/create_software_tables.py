#!/usr/bin/env python3
"""
Script para criar as novas tabelas de software no banco de dados
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models.database import db, SoftwareGroup, SoftwareGroupItem, SoftwareGroupAsset, SoftwareInstallationStatus

def create_software_tables():
    """Cria as novas tabelas de software"""
    
    print("=== CRIANDO TABELAS DE SOFTWARE ===")
    
    with app.app_context():
        try:
            # Criar as tabelas
            db.create_all()
            
            print("✅ Tabelas criadas com sucesso!")
            print("\n📋 Tabelas criadas:")
            print("  • software_groups - Grupos de software")
            print("  • software_group_items - Itens de software nos grupos")
            print("  • software_group_assets - Assets atribuídos aos grupos")
            print("  • software_installation_status - Status de instalação")
            
            # Verificar se as tabelas foram criadas
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            software_tables = [table for table in tables if 'software' in table.lower()]
            
            print(f"\n🔍 Tabelas de software encontradas: {len(software_tables)}")
            for table in software_tables:
                print(f"  ✅ {table}")
            
            # Criar alguns dados de exemplo
            create_sample_data()
            
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            import traceback
            traceback.print_exc()

def create_sample_data():
    """Cria dados de exemplo para as tabelas"""
    
    print("\n=== CRIANDO DADOS DE EXEMPLO ===")
    
    try:
        # Criar grupos de software de exemplo
        groups = [
            {
                'name': 'Software Básico',
                'description': 'Software essencial para todos os computadores',
                'is_required': True
            },
            {
                'name': 'Software de Desenvolvimento',
                'description': 'Ferramentas para desenvolvedores',
                'is_required': False
            },
            {
                'name': 'Software de Segurança',
                'description': 'Antivírus e ferramentas de segurança',
                'is_required': True
            }
        ]
        
        for group_data in groups:
            group = SoftwareGroup(**group_data)
            db.session.add(group)
        
        db.session.commit()
        print("✅ Grupos de software criados")
        
        # Criar alguns status de instalação de exemplo
        status_examples = [
            {
                'software_name': 'Microsoft Office',
                'software_vendor': 'Microsoft Corporation',
                'software_version': '16.0.18925.20158',
                'action_type': 'install',
                'status': 'completed',
                'error_message': None
            },
            {
                'software_name': 'Adobe Reader',
                'software_vendor': 'Adobe Systems',
                'software_version': '11.0.23',
                'action_type': 'install',
                'status': 'failed',
                'error_message': 'Erro de permissão durante a instalação'
            },
            {
                'software_name': 'Chrome',
                'software_vendor': 'Google',
                'software_version': '120.0.6099.109',
                'action_type': 'update',
                'status': 'blocked',
                'blocked_reason': 'Usuário não autorizado para atualizações'
            }
        ]
        
        for status_data in status_examples:
            status = SoftwareInstallationStatus(**status_data)
            db.session.add(status)
        
        db.session.commit()
        print("✅ Status de instalação criados")
        
        print("\n📊 Resumo dos dados criados:")
        print(f"  • Grupos de software: {SoftwareGroup.query.count()}")
        print(f"  • Status de instalação: {SoftwareInstallationStatus.query.count()}")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados de exemplo: {e}")
        db.session.rollback()

def verify_tables():
    """Verifica se as tabelas foram criadas corretamente"""
    
    print("\n=== VERIFICANDO TABELAS ===")
    
    with app.app_context():
        try:
            # Verificar estrutura das tabelas
            inspector = db.inspect(db.engine)
            
            tables_to_check = [
                'software_groups',
                'software_group_items', 
                'software_group_assets',
                'software_installation_status'
            ]
            
            for table_name in tables_to_check:
                if inspector.has_table(table_name):
                    columns = inspector.get_columns(table_name)
                    print(f"✅ {table_name}: {len(columns)} colunas")
                    for column in columns:
                        print(f"    - {column['name']}: {column['type']}")
                else:
                    print(f"❌ Tabela {table_name} não encontrada")
            
            # Verificar relacionamentos
            print("\n🔗 Verificando relacionamentos:")
            
            # Testar consultas básicas
            group_count = SoftwareGroup.query.count()
            status_count = SoftwareInstallationStatus.query.count()
            
            print(f"  • Grupos de software: {group_count}")
            print(f"  • Status de instalação: {status_count}")
            
            if group_count > 0:
                sample_group = SoftwareGroup.query.first()
                if sample_group:
                    print(f"  • Exemplo de grupo: {sample_group.name}")
            
            if status_count > 0:
                sample_status = SoftwareInstallationStatus.query.first()
                if sample_status:
                    print(f"  • Exemplo de status: {sample_status.software_name} - {sample_status.status}")
            
        except Exception as e:
            print(f"❌ Erro ao verificar tabelas: {e}")

if __name__ == "__main__":
    print("🧪 SCRIPT DE CRIAÇÃO DAS TABELAS DE SOFTWARE")
    print("=" * 60)
    
    create_software_tables()
    verify_tables()
    
    print("\n" + "=" * 60)
    print("✅ Script concluído!")
    print("\n📋 PRÓXIMOS PASSOS:")
    print("  1. Verificar se as tabelas foram criadas no banco")
    print("  2. Testar as funcionalidades da página de software")
    print("  3. Configurar permissões se necessário")
    print("  4. Adicionar dados reais conforme necessário") 
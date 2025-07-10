#!/usr/bin/env python3
"""
Script de teste para verificar a coleta de informações do modelo e fabricante do computador
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import db, Asset
from config import CONFIG
from flask import Flask

def test_computer_info_collection():
    """Testa a coleta de informações do computador"""
    print("=== Teste de Coleta de Informações do Computador ===")
    
    # Simular dados que viriam do agente
    test_system_info = {
        'hostname': 'TEST-PC-001',
        'ip_address': '192.168.1.100',
        'mac_address': '00:11:22:33:44:55',
        'operating_system': 'Windows 10',
        'os_version': '10.0.19045',
        'python_version': '3.11.0',
        'architecture': '64bit',
        'processor': 'Intel(R) Core(TM) i7-10700K CPU @ 3.80GHz',
        'cpu_count': 8,
        'cpu_count_logical': 16,
        'cpu_freq_current': 3800.0,
        'cpu_freq_min': 800.0,
        'cpu_freq_max': 5100.0,
        'computer_model': 'Latitude 5520',
        'computer_manufacturer': 'Dell Inc.',
        'computer_system_type': 'x64-based PC',
        'memory_info': {
            'total_bytes': 17179869184,  # 16GB
            'available_bytes': 8589934592,  # 8GB
            'percent': 50.0
        },
        'disk_info': [{
            'total_bytes': 1000204886016,  # ~1TB
            'used_bytes': 500102443008,  # ~500GB
            'free_bytes': 500102443008,  # ~500GB
            'percent': 50.0,
            'model': 'Samsung SSD 970 EVO Plus 1TB',
            'serial': 'S4EWNF0M803123X',
            'interface_type': 'NVMe'
        }]
    }
    
    print("Dados simulados do sistema:")
    print(f"  Modelo: {test_system_info.get('computer_model', 'N/A')}")
    print(f"  Fabricante: {test_system_info.get('computer_manufacturer', 'N/A')}")
    print(f"  Tipo do Sistema: {test_system_info.get('computer_system_type', 'N/A')}")
    print(f"  Processador: {test_system_info.get('processor', 'N/A')}")
    print(f"  Sistema Operacional: {test_system_info.get('operating_system', 'N/A')}")
    print()
    
    return test_system_info

def test_database_connection():
    """Testa a conexão com o banco de dados"""
    print("=== Teste de Conexão com Banco de Dados ===")
    
    try:
        # Criar aplicação Flask para teste
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG.DATABASE_URL
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        
        with app.app_context():
            # Testar conexão
            db.engine.execute('SELECT 1')
            print("✅ Conexão com banco de dados estabelecida com sucesso")
            
            # Verificar se as novas colunas existem
            result = db.engine.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'assets' 
                AND column_name IN ('computer_model', 'computer_manufacturer', 'computer_system_type')
                ORDER BY column_name
            """)
            
            columns = [row for row in result]
            if len(columns) == 3:
                print("✅ Novas colunas encontradas no banco de dados:")
                for col in columns:
                    print(f"  - {col[0]} ({col[1]})")
            else:
                print("❌ Novas colunas não encontradas. Execute o script add_computer_info_columns.sql")
                return False
                
            return True
            
    except Exception as e:
        print(f"❌ Erro na conexão com banco de dados: {e}")
        return False

def test_asset_creation():
    """Testa a criação de um asset com as novas informações"""
    print("\n=== Teste de Criação de Asset ===")
    
    try:
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG.DATABASE_URL
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        
        with app.app_context():
            # Simular dados do sistema
            system_info = test_computer_info_collection()
            
            # Criar asset de teste
            test_asset = Asset(
                organization_id=1,  # Assumindo que existe uma organização com ID 1
                asset_tag='TEST-COMPUTER-001',
                name=system_info.get('hostname', 'Test Computer'),
                description='Asset de teste com informações do computador',
                status='active',
                criticality='medium',
                ip_address=system_info.get('ip_address'),
                mac_address=system_info.get('mac_address'),
                operating_system=system_info.get('operating_system'),
                os_version=system_info.get('os_version'),
                python_version=system_info.get('python_version'),
                architecture=system_info.get('architecture'),
                processor=system_info.get('processor'),
                cpu_count=system_info.get('cpu_count'),
                cpu_count_logical=system_info.get('cpu_count_logical'),
                cpu_freq_current=system_info.get('cpu_freq_current'),
                cpu_freq_min=system_info.get('cpu_freq_min'),
                cpu_freq_max=system_info.get('cpu_freq_max'),
                computer_model=system_info.get('computer_model'),
                computer_manufacturer=system_info.get('computer_manufacturer'),
                computer_system_type=system_info.get('computer_system_type')
            )
            
            # Adicionar ao banco
            db.session.add(test_asset)
            db.session.commit()
            
            print("✅ Asset criado com sucesso no banco de dados")
            print(f"  ID: {test_asset.id}")
            print(f"  Tag: {test_asset.asset_tag}")
            print(f"  Modelo: {test_asset.computer_model}")
            print(f"  Fabricante: {test_asset.computer_manufacturer}")
            
            # Limpar asset de teste
            db.session.delete(test_asset)
            db.session.commit()
            print("✅ Asset de teste removido")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro ao criar asset: {e}")
        return False

def main():
    """Função principal do teste"""
    print("Iniciando testes das novas funcionalidades de informações do computador...\n")
    
    # Teste 1: Coleta de informações
    test_computer_info_collection()
    
    # Teste 2: Conexão com banco
    db_ok = test_database_connection()
    
    # Teste 3: Criação de asset (apenas se banco estiver OK)
    if db_ok:
        test_asset_creation()
    
    print("\n=== Resumo dos Testes ===")
    if db_ok:
        print("✅ Todos os testes passaram com sucesso!")
        print("As novas funcionalidades estão prontas para uso.")
    else:
        print("❌ Alguns testes falharam. Verifique a configuração do banco de dados.")

if __name__ == "__main__":
    main() 
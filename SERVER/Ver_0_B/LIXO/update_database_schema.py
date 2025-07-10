#!/usr/bin/env python3
"""
Script para atualizar o esquema do banco de dados com as novas colunas de informações do computador
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from config import CONFIG
from models.database import db

def update_database_schema():
    """Atualiza o esquema do banco de dados com as novas colunas"""
    print("=== Atualização do Esquema do Banco de Dados ===")
    
    # Criar aplicação Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG.DATABASE_URL_DEFAULT
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        try:
            # Verificar se as colunas já existem
            result = db.engine.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'assets' 
                AND column_name IN ('computer_model', 'computer_manufacturer', 'computer_system_type')
                ORDER BY column_name
            """)
            
            existing_columns = [row[0] for row in result]
            print(f"Colunas existentes: {existing_columns}")
            
            # Adicionar colunas que não existem
            columns_to_add = []
            if 'computer_model' not in existing_columns:
                columns_to_add.append('computer_model VARCHAR(255)')
            if 'computer_manufacturer' not in existing_columns:
                columns_to_add.append('computer_manufacturer VARCHAR(255)')
            if 'computer_system_type' not in existing_columns:
                columns_to_add.append('computer_system_type VARCHAR(100)')
            
            if columns_to_add:
                print(f"Adicionando colunas: {columns_to_add}")
                
                # Adicionar cada coluna
                for column_def in columns_to_add:
                    column_name = column_def.split()[0]
                    sql = f"ALTER TABLE assets ADD COLUMN {column_def}"
                    print(f"Executando: {sql}")
                    db.engine.execute(sql)
                    print(f"✅ Coluna {column_name} adicionada com sucesso")
                
                print("\n✅ Todas as colunas foram adicionadas com sucesso!")
            else:
                print("✅ Todas as colunas já existem no banco de dados")
            
            # Verificar novamente
            result = db.engine.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'assets' 
                AND column_name IN ('computer_model', 'computer_manufacturer', 'computer_system_type')
                ORDER BY column_name
            """)
            
            print("\n=== Verificação Final ===")
            for row in result:
                print(f"  - {row[0]} ({row[1]})")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao atualizar esquema: {e}")
            return False

def test_asset_model():
    """Testa se o modelo Asset pode ser usado com as novas colunas"""
    print("\n=== Teste do Modelo Asset ===")
    
    try:
        from models.database import Asset
        
        # Criar uma instância de teste (sem salvar)
        test_asset = Asset(
            organization_id=1,
            asset_tag='TEST-001',
            name='Test Asset',
            computer_model='Test Model',
            computer_manufacturer='Test Manufacturer',
            computer_system_type='Test System Type'
        )
        
        print("✅ Modelo Asset aceita as novas colunas")
        print(f"  Modelo: {test_asset.computer_model}")
        print(f"  Fabricante: {test_asset.computer_manufacturer}")
        print(f"  Tipo do Sistema: {test_asset.computer_system_type}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no modelo Asset: {e}")
        return False

def main():
    """Função principal"""
    print("Iniciando atualização do esquema do banco de dados...\n")
    
    # Atualizar esquema
    schema_ok = update_database_schema()
    
    if schema_ok:
        # Testar modelo
        model_ok = test_asset_model()
        
        print("\n=== Resumo ===")
        if schema_ok and model_ok:
            print("✅ Atualização concluída com sucesso!")
            print("O banco de dados está pronto para receber as novas informações do computador.")
        else:
            print("❌ Alguns problemas foram encontrados durante a atualização.")
    else:
        print("❌ Falha na atualização do esquema.")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Script para executar migrações do banco de dados
Adiciona as tabelas necessárias para o sistema de gerenciamento de software
"""

import os
import sys
import psycopg2
from config import CONFIG

def run_migrations():
    """Executa as migrações do banco de dados"""
    
    # Conectar ao banco de dados
    try:
        conn = psycopg2.connect(CONFIG.DATABASE_URL_DEFAULT)
        cursor = conn.cursor()
        print("✅ Conectado ao banco de dados PostgreSQL")
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")
        return False
    
    # Ler o arquivo de esquema
    schema_file = os.path.join(os.path.dirname(__file__), 'models', 'software_management_schema.sql')
    
    try:
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        print("✅ Arquivo de esquema carregado")
    except Exception as e:
        print(f"❌ Erro ao carregar arquivo de esquema: {e}")
        return False
    
    # Executar as migrações
    try:
        # Dividir o SQL em comandos individuais
        commands = schema_sql.split(';')
        
        for command in commands:
            command = command.strip()
            if command and not command.startswith('--'):
                try:
                    cursor.execute(command)
                    print(f"✅ Executado: {command[:50]}...")
                except Exception as e:
                    if "already exists" in str(e).lower():
                        print(f"⚠️  Tabela já existe: {command[:50]}...")
                    else:
                        print(f"❌ Erro ao executar comando: {e}")
                        print(f"Comando: {command}")
                        return False
        
        # Commit das alterações
        conn.commit()
        print("✅ Migrações executadas com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante execução das migrações: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
    
    return True

def check_tables():
    """Verifica se as tabelas foram criadas corretamente"""
    
    try:
        conn = psycopg2.connect(CONFIG.DATABASE_URL_DEFAULT)
        cursor = conn.cursor()
        
        # Lista de tabelas esperadas
        expected_tables = [
            'software_groups',
            'software_group_items',
            'software_group_assets',
            'software_installation_status',
            'software_policies',
            'software_execution_logs'
        ]
        
        print("\n📋 Verificando tabelas criadas:")
        
        for table in expected_tables:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                );
            """, (table,))
            
            exists = cursor.fetchone()[0]
            if exists:
                print(f"✅ {table}")
            else:
                print(f"❌ {table} - NÃO ENCONTRADA")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao verificar tabelas: {e}")

if __name__ == '__main__':
    print("🚀 Iniciando migrações do sistema de gerenciamento de software...")
    print("=" * 60)
    
    success = run_migrations()
    
    if success:
        print("\n" + "=" * 60)
        check_tables()
        print("\n🎉 Migrações concluídas com sucesso!")
        print("O sistema de gerenciamento de software está pronto para uso.")
    else:
        print("\n❌ Falha nas migrações. Verifique os erros acima.")
        sys.exit(1) 
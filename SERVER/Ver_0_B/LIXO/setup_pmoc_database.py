#!/usr/bin/env python3
"""
Script para configurar o banco de dados PMOC
Cria o banco de dados se não existir e configura as permissões
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy import create_engine, text
from modulos.pmoc.pmoc_config import CONFIG_PMOC

# NOVO: Importar psycopg2 para criar o banco com autocommit
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    """Cria o banco de dados DB_PMOC_1 se não existir"""
    
    # URL para conectar ao PostgreSQL sem especificar banco
    base_url = f"postgresql://{CONFIG_PMOC.DB_USER}:{CONFIG_PMOC.DB_PASSWORD}@{CONFIG_PMOC.DB_HOST}:{CONFIG_PMOC.DB_PORT}/postgres"
    
    try:
        print("🔍 Conectando ao PostgreSQL...")
        # Usar psycopg2 para garantir autocommit
        conn = psycopg2.connect(
            dbname='postgres',
            user=CONFIG_PMOC.DB_USER,
            password=CONFIG_PMOC.DB_PASSWORD,
            host=CONFIG_PMOC.DB_HOST,
            port=CONFIG_PMOC.DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        # Verificar se o banco DB_PMOC_1 existe
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'DB_PMOC_1'")
        db_exists = cur.fetchone()
        if db_exists:
            print("✅ Banco de dados 'DB_PMOC_1' já existe!")
            cur.close()
            conn.close()
            return True
        else:
            print("📋 Criando banco de dados 'DB_PMOC_1'...")
            cur.execute("CREATE DATABASE DB_PMOC_1")
            print("✅ Banco de dados 'DB_PMOC_1' criado com sucesso!")
            cur.close()
            conn.close()
            return True
    except Exception as e:
        print(f"❌ Erro ao criar banco de dados: {e}")
        return False

def verify_user_permissions():
    """Verifica se o usuário isac tem as permissões necessárias"""
    
    try:
        print("🔍 Verificando permissões do usuário...")
        # Conectar ao banco DB_PMOC_1
        engine = create_engine(CONFIG_PMOC.DATABASE_URL)
        with engine.connect() as conn:
            # Verificar se o usuário pode criar tabelas
            result = conn.execute(text("""
                SELECT has_table_privilege('isac', 'information_schema.tables', 'SELECT')
            """))
            can_select = result.scalar()
            if can_select:
                print("✅ Usuário 'isac' tem permissões adequadas!")
                return True
            else:
                print("⚠️  Usuário 'isac' pode não ter todas as permissões necessárias")
                print("   Execute manualmente no PostgreSQL:")
                print("   GRANT ALL PRIVILEGES ON DATABASE DB_PMOC_1 TO isac;")
                print("   GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO isac;")
                return False
    except Exception as e:
        print(f"❌ Erro ao verificar permissões: {e}")
        return False

def test_connection():
    """Testa a conexão com o banco DB_PMOC_1"""
    try:
        print("🔍 Testando conexão com DB_PMOC_1...")
        engine = create_engine(CONFIG_PMOC.DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexão com DB_PMOC_1 estabelecida com sucesso!")
            return True
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def main():
    """Executa a configuração completa do banco de dados"""
    print("🔧 Configuração do Banco de Dados PMOC")
    print("=" * 50)
    # Passo 1: Criar banco de dados
    if not create_database():
        print("\n❌ Falha ao criar banco de dados.")
        print("   Verifique se:")
        print("   1. O PostgreSQL está rodando")
        print("   2. O usuário 'isac' existe e tem permissões de CREATE DATABASE")
        print("   3. As credenciais estão corretas")
        sys.exit(1)
    # Passo 2: Verificar permissões
    verify_user_permissions()
    # Passo 3: Testar conexão
    if not test_connection():
        print("\n❌ Falha na conexão com DB_PMOC_1.")
        sys.exit(1)
    print("\n✅ Configuração do banco de dados concluída!")
    print("   Agora você pode executar:")
    print("   python create_pmoc_tables.py")

if __name__ == "__main__":
    main() 
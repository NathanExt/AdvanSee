#!/usr/bin/env python3
"""
Script completo para gravar dados dos notebooks no banco DB_PMOC_1
Versão 2.0 - Mais robusta
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy import create_engine, text
from modulos.pmoc.pmoc_config import CONFIG_PMOC
from modulos.pmoc.pmoc_models.pmoc_database import Base
from modulos.pmoc.pmoc_main import PMOC

# Importar psycopg2 para criar o banco com autocommit
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    """Cria o banco de dados DB_PMOC_1 se não existir"""
    
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
        else:
            print("📋 Criando banco de dados 'DB_PMOC_1'...")
            cur.execute("CREATE DATABASE DB_PMOC_1")
            print("✅ Banco de dados 'DB_PMOC_1' criado com sucesso!")
        
        # Aguardar um pouco para o banco estar disponível
        print("⏳ Aguardando banco ficar disponível...")
        time.sleep(3)
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar banco de dados: {e}")
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

def create_tables():
    """Cria as tabelas necessárias"""
    try:
        print("📋 Criando tabelas...")
        engine = create_engine(CONFIG_PMOC.DATABASE_URL)
        
        with engine.connect() as conn:
            # Verificar se a tabela notebook já existe
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'notebook'
                );
            """))
            
            table_exists = result.scalar()
            
            if table_exists:
                print("✅ Tabela 'notebook' já existe!")
                return True
            else:
                print("📋 Criando tabela 'notebook'...")
                
                # Criar a tabela usando SQLAlchemy
                Base.metadata.create_all(engine)
                
                print("✅ Tabela 'notebook' criada com sucesso!")
                return True
                
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        return False

def gravar_dados():
    """Grava os dados dos notebooks"""
    try:
        print("📊 Gravando dados dos notebooks...")
        pmoc = PMOC()
        pmoc.grava_dados()
        return True
    except Exception as e:
        print(f"❌ Erro durante a gravação: {e}")
        return False

def main():
    """Executa o processo completo"""
    
    print("🚀 Processo de Gravação de Notebooks - DB_PMOC_1")
    print("=" * 60)
    
    # Passo 1: Criar banco de dados
    print("\n📋 PASSO 1: Configurando banco de dados...")
    if not create_database():
        print("❌ Falha ao criar banco de dados.")
        return False
    
    # Passo 2: Testar conexão (com retry)
    print("\n🔍 PASSO 2: Testando conexão...")
    for attempt in range(3):
        if test_connection():
            break
        else:
            if attempt < 2:
                print(f"   Tentativa {attempt + 1} falhou. Aguardando 5 segundos...")
                time.sleep(5)
            else:
                print("❌ Falha na conexão após 3 tentativas.")
                return False
    
    # Passo 3: Criar tabelas
    print("\n📋 PASSO 3: Criando tabelas...")
    if not create_tables():
        print("❌ Falha ao criar tabelas.")
        return False
    
    # Passo 4: Gravar dados
    print("\n📊 PASSO 4: Gravando dados dos notebooks...")
    if not gravar_dados():
        print("❌ Falha na gravação dos dados.")
        return False
    
    print("\n✅ Processo concluído com sucesso!")
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Todos os dados foram gravados no banco DB_PMOC_1!")
    else:
        print("\n❌ Ocorreu um erro durante o processo.")
        sys.exit(1) 
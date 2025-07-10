#!/usr/bin/env python3
"""
Script para criar as tabelas do módulo PMOC no banco de dados DB_PMOC
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy import create_engine, text
from modulos.pmoc.pmoc_config import CONFIG_PMOC
from modulos.pmoc.pmoc_models.pmoc_database import Base

def create_pmoc_tables():
    """Cria as tabelas do módulo PMOC no banco de dados"""
    
    try:
        # Criar engine de conexão
        engine = create_engine(CONFIG_PMOC.DATABASE_URL)
        
        # Verificar se o banco existe
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
                print("✅ Tabela 'notebook' já existe no banco de dados DB_PMOC_1")
                return True
            else:
                print("📋 Criando tabela 'notebook' no banco de dados DB_PMOC_1...")
                
                # Criar a tabela usando SQLAlchemy
                Base.metadata.create_all(engine)
                
                print("✅ Tabela 'notebook' criada com sucesso!")
                return True
                
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        return False

def verify_connection():
    """Verifica se é possível conectar ao banco de dados"""
    
    try:
        engine = create_engine(CONFIG_PMOC.DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexão com o banco de dados DB_PMOC estabelecida com sucesso!")
            return True
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")
        print(f"   URL: {CONFIG_PMOC.DATABASE_URL}")
        return False

if __name__ == "__main__":
    print("🔧 Script de criação das tabelas PMOC")
    print("=" * 50)
    
    # Verificar conexão
    if not verify_connection():
        print("\n❌ Não foi possível conectar ao banco de dados.")
        print("   Verifique se:")
        print("   1. O PostgreSQL está rodando")
        print("   2. O banco 'DB_PMOC' existe")
        print("   3. O usuário 'isac' tem permissões")
        print("   4. As credenciais estão corretas")
        sys.exit(1)
    
    # Criar tabelas
    if create_pmoc_tables():
        print("\n✅ Processo concluído com sucesso!")
        print("   Agora você pode executar o módulo PMOC para gravar os dados.")
    else:
        print("\n❌ Falha ao criar as tabelas.")
        sys.exit(1) 
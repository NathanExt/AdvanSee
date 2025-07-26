#!/usr/bin/env python3
"""
Script para configurar o banco de dados DB_USERS e criar a tabela ad_users
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import CONFIG

def create_database():
    """Cria o banco de dados DB_USERS se não existir"""
    
    try:
        print("🔍 Conectando ao PostgreSQL...")
        # Usar psycopg2 para garantir autocommit
        conn = psycopg2.connect(
            dbname='postgres',
            user=CONFIG.DB_USER,
            password=CONFIG.DB_PASSWORD,
            host=CONFIG.DB_HOST,
            port=CONFIG.DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Verificar se o banco DB_USERS existe
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'DB_USERS'")
        db_exists = cur.fetchone()
        
        if db_exists:
            print("✅ Banco de dados 'DB_USERS' já existe!")
        else:
            print("📋 Criando banco de dados 'DB_USERS'...")
            cur.execute("CREATE DATABASE DB_USERS")
            print("✅ Banco de dados 'DB_USERS' criado com sucesso!")
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar banco de dados: {e}")
        return False

def create_ad_users_table():
    """Cria a tabela ad_users no banco DB_USERS"""
    
    try:
        print("🔍 Conectando ao banco DB_USERS...")
        conn = psycopg2.connect(
            dbname='DB_USERS',
            user=CONFIG.DB_USER,
            password=CONFIG.DB_PASSWORD,
            host=CONFIG.DB_HOST,
            port=CONFIG.DB_PORT
        )
        cur = conn.cursor()
        
        # Verificar se a tabela ad_users existe
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'ad_users'
            );
        """)
        table_exists = cur.fetchone()[0]
        
        if table_exists:
            print("✅ Tabela 'ad_users' já existe!")
        else:
            print("📋 Criando tabela 'ad_users'...")
            
            # Criar a tabela ad_users
            cur.execute("""
                CREATE TABLE ad_users (
                    id SERIAL PRIMARY KEY,
                    display_name VARCHAR(255),
                    sam_account_name VARCHAR(255) UNIQUE NOT NULL,
                    given_name VARCHAR(255),
                    surname VARCHAR(255),
                    email_address VARCHAR(255),
                    enabled BOOLEAN,
                    last_logon_date TIMESTAMP,
                    distinguished_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Criar índices para melhorar performance
            cur.execute("CREATE INDEX idx_email_address ON ad_users(email_address);")
            cur.execute("CREATE INDEX idx_display_name ON ad_users(display_name);")
            cur.execute("CREATE INDEX idx_enabled ON ad_users(enabled);")
            cur.execute("CREATE INDEX idx_last_logon ON ad_users(last_logon_date);")
            
            # Trigger para atualizar o campo updated_at automaticamente
            cur.execute("""
                CREATE OR REPLACE FUNCTION update_updated_at_column()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated_at = CURRENT_TIMESTAMP;
                    RETURN NEW;
                END;
                $$ language 'plpgsql';
            """)
            
            cur.execute("""
                CREATE TRIGGER update_ad_users_updated_at BEFORE UPDATE
                ON ad_users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
            """)
            
            conn.commit()
            print("✅ Tabela 'ad_users' criada com sucesso!")
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar tabela: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Configurando banco de dados para usuários AD...")
    
    # Criar banco de dados
    if create_database():
        # Criar tabela
        if create_ad_users_table():
            print("✅ Configuração concluída com sucesso!")
            print("📋 Banco DB_USERS e tabela ad_users estão prontos para uso.")
        else:
            print("❌ Erro ao criar tabela ad_users")
    else:
        print("❌ Erro ao criar banco de dados DB_USERS")

if __name__ == "__main__":
    main() 
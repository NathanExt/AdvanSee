-- Schema para armazenar informações de usuários do Active Directory
-- Criar o banco de dados (executar como superusuário)
-- CREATE DATABASE ad_users_db;

-- Conectar ao banco e criar a tabela
CREATE TABLE IF NOT EXISTS ad_users (
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

-- Criar índices para melhorar performance
CREATE INDEX idx_email_address ON ad_users(email_address);
CREATE INDEX idx_display_name ON ad_users(display_name);
CREATE INDEX idx_enabled ON ad_users(enabled);
CREATE INDEX idx_last_logon ON ad_users(last_logon_date);

-- Trigger para atualizar o campo updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_ad_users_updated_at BEFORE UPDATE
    ON ad_users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
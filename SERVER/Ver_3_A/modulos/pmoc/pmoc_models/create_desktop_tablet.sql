-- Script para criar a tabela desktop no banco de dados DB_PMOC
-- Execute este script no PostgreSQL para criar a tabela


-- Verificar se a tabela já existe
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'desktop') THEN
        
        -- Criar a tabela desktop
        CREATE TABLE desktop (
            id VARCHAR PRIMARY KEY,
            model TEXT,
            patrimony VARCHAR,
            manufacturer TEXT,
            equipment_value NUMERIC(10, 2),
            tag_uisa VARCHAR,
            created_at DATE,
            updated_by VARCHAR,
            tag VARCHAR,
            os_version TEXT,
            entry_note VARCHAR,
            status VARCHAR,
            date_home DATE,
            date_end DATE,
            updated_at TIMESTAMP,
            rc VARCHAR,
            owner VARCHAR,
            processor TEXT,
            type VARCHAR,
            ram_memory VARCHAR,
            last_inventory_date DATE,
            contract_type VARCHAR,
            os_architecture VARCHAR
        );
        
        -- Criar índices para melhor performance
        CREATE INDEX idx_desktop_patrimony ON desktop(patrimony);
        CREATE INDEX idx_desktop_owner ON desktop(owner);
        CREATE INDEX idx_desktop_status ON desktop(status);
        CREATE INDEX idx_desktop_created_at ON desktop(created_at);
        
        RAISE NOTICE 'Tabela desktop criada com sucesso!';
    ELSE
        RAISE NOTICE 'Tabela desktop já existe!';
    END IF;
END $$;

-- Verificar se a tabela foi criada
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'desktop' 
ORDER BY ordinal_position; 
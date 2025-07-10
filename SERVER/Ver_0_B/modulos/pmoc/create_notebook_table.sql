-- Script para criar a tabela notebook no banco de dados DB_PMOC
-- Execute este script no PostgreSQL para criar a tabela

-- Verificar se a tabela já existe
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'notebook') THEN
        
        -- Criar a tabela notebook
        CREATE TABLE notebook (
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
        CREATE INDEX idx_notebook_patrimony ON notebook(patrimony);
        CREATE INDEX idx_notebook_owner ON notebook(owner);
        CREATE INDEX idx_notebook_status ON notebook(status);
        CREATE INDEX idx_notebook_created_at ON notebook(created_at);
        
        RAISE NOTICE 'Tabela notebook criada com sucesso!';
    ELSE
        RAISE NOTICE 'Tabela notebook já existe!';
    END IF;
END $$;

-- Verificar se a tabela foi criada
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'notebook' 
ORDER BY ordinal_position; 
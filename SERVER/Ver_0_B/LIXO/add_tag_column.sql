-- Script de migração para adicionar a coluna 'tag' na tabela assets
-- Execute este script no banco de dados DB_ASSETS para adicionar a nova coluna

-- Adicionar a coluna tag na tabela assets
ALTER TABLE assets 
ADD COLUMN tag VARCHAR(255);

-- Adicionar um comentário para documentar a coluna
COMMENT ON COLUMN assets.tag IS 'Tag do asset obtida do agente através do SerialNumber da BIOS';

-- Verificar se a coluna foi adicionada corretamente
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'assets' AND column_name = 'tag';

-- Comando para reverter a migração (caso necessário)
-- ALTER TABLE assets DROP COLUMN tag; 
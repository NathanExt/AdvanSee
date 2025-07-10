-- Script para adicionar colunas de informações do computador à tabela assets
-- Execute este script no banco de dados PostgreSQL

-- Adicionar colunas para informações do modelo e fabricante do computador
ALTER TABLE assets 
ADD COLUMN IF NOT EXISTS computer_model VARCHAR(255),
ADD COLUMN IF NOT EXISTS computer_manufacturer VARCHAR(255),
ADD COLUMN IF NOT EXISTS computer_system_type VARCHAR(100);

-- Comentários para documentar as novas colunas
COMMENT ON COLUMN assets.computer_model IS 'Modelo do computador (ex: Latitude 5520, ThinkPad X1 Carbon)';
COMMENT ON COLUMN assets.computer_manufacturer IS 'Fabricante do computador (ex: Dell, Lenovo, HP)';
COMMENT ON COLUMN assets.computer_system_type IS 'Tipo do sistema (ex: x64-based PC, ARM-based PC)';

-- Verificar se as colunas foram adicionadas
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'assets' 
AND column_name IN ('computer_model', 'computer_manufacturer', 'computer_system_type')
ORDER BY column_name; 
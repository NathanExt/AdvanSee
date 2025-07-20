-- Script para criar a tabela pmoc_assets
-- Execute este script no seu banco de dados PostgreSQL

-- Tabela para armazenar ativos encontrados no PMOC
CREATE TABLE IF NOT EXISTS pmoc_assets (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(id) ON DELETE CASCADE,
    pmoc_type VARCHAR(50) NOT NULL, -- 'notebook' ou 'desktop'
    pmoc_id VARCHAR(255), -- ID do equipamento no PMOC
    tag VARCHAR(255), -- Tag do equipamento no PMOC
    tag_uisa VARCHAR(255), -- Tag UISA do equipamento
    patrimony VARCHAR(255), -- Número do patrimônio
    manufacturer VARCHAR(255), -- Fabricante
    model VARCHAR(255), -- Modelo
    serial_number VARCHAR(255), -- Número de série
    user_name VARCHAR(255), -- Nome do usuário
    department VARCHAR(255), -- Departamento
    location VARCHAR(255), -- Localização
    status VARCHAR(100), -- Status no PMOC
    last_sync TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Última sincronização
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(asset_id, pmoc_type, pmoc_id)
);

-- Índices para melhorar performance
CREATE INDEX IF NOT EXISTS idx_pmoc_assets_asset_id ON pmoc_assets(asset_id);
CREATE INDEX IF NOT EXISTS idx_pmoc_assets_pmoc_type ON pmoc_assets(pmoc_type);
CREATE INDEX IF NOT EXISTS idx_pmoc_assets_tag ON pmoc_assets(tag);
CREATE INDEX IF NOT EXISTS idx_pmoc_assets_tag_uisa ON pmoc_assets(tag_uisa);
CREATE INDEX IF NOT EXISTS idx_pmoc_assets_patrimony ON pmoc_assets(patrimony);
CREATE INDEX IF NOT EXISTS idx_pmoc_assets_last_sync ON pmoc_assets(last_sync);

-- Comentários na tabela
COMMENT ON TABLE pmoc_assets IS 'Tabela para armazenar ativos encontrados no PMOC';
COMMENT ON COLUMN pmoc_assets.asset_id IS 'ID do asset no banco local';
COMMENT ON COLUMN pmoc_assets.pmoc_type IS 'Tipo do equipamento no PMOC (notebook ou desktop)';
COMMENT ON COLUMN pmoc_assets.pmoc_id IS 'ID do equipamento no PMOC';
COMMENT ON COLUMN pmoc_assets.tag IS 'Tag do equipamento no PMOC';
COMMENT ON COLUMN pmoc_assets.tag_uisa IS 'Tag UISA do equipamento';
COMMENT ON COLUMN pmoc_assets.patrimony IS 'Número do patrimônio';
COMMENT ON COLUMN pmoc_assets.manufacturer IS 'Fabricante do equipamento';
COMMENT ON COLUMN pmoc_assets.model IS 'Modelo do equipamento';
COMMENT ON COLUMN pmoc_assets.serial_number IS 'Número de série';
COMMENT ON COLUMN pmoc_assets.user_name IS 'Nome do usuário';
COMMENT ON COLUMN pmoc_assets.department IS 'Departamento';
COMMENT ON COLUMN pmoc_assets.location IS 'Localização';
COMMENT ON COLUMN pmoc_assets.status IS 'Status no PMOC';
COMMENT ON COLUMN pmoc_assets.last_sync IS 'Data/hora da última sincronização'; 
-- esquema_grupos_assets.sql
-- Script para criar as tabelas necessárias para grupos de assets (PostgreSQL)

-- Tabela de grupos de assets
CREATE TABLE IF NOT EXISTS asset_groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    is_active BOOLEAN DEFAULT TRUE
);

-- Índices para asset_groups
CREATE INDEX IF NOT EXISTS idx_asset_groups_name ON asset_groups(name);
CREATE INDEX IF NOT EXISTS idx_asset_groups_active ON asset_groups(is_active);
CREATE INDEX IF NOT EXISTS idx_asset_groups_created_at ON asset_groups(created_at);

-- Tabela de relacionamento entre grupos e assets
CREATE TABLE IF NOT EXISTS asset_group_items (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL,
    asset_id INTEGER NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    added_by INTEGER,
    CONSTRAINT fk_group_id FOREIGN KEY (group_id) REFERENCES asset_groups(id) ON DELETE CASCADE,
    CONSTRAINT fk_asset_id FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE,
    CONSTRAINT unique_group_asset UNIQUE (group_id, asset_id)
);

-- Índices para asset_group_items
CREATE INDEX IF NOT EXISTS idx_asset_group_items_group ON asset_group_items(group_id);
CREATE INDEX IF NOT EXISTS idx_asset_group_items_asset ON asset_group_items(asset_id);
CREATE INDEX IF NOT EXISTS idx_asset_group_items_added_at ON asset_group_items(added_at);

-- Tabela de configurações/políticas do grupo (para uso futuro)
CREATE TABLE IF NOT EXISTS asset_group_policies (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL,
    policy_type VARCHAR(50) NOT NULL, -- 'software', 'update', 'security', etc
    policy_name VARCHAR(255) NOT NULL,
    policy_value TEXT,
    is_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_policy_group_id FOREIGN KEY (group_id) REFERENCES asset_groups(id) ON DELETE CASCADE
);

-- Índices para asset_group_policies
CREATE INDEX IF NOT EXISTS idx_asset_group_policies_group_policy ON asset_group_policies(group_id, policy_type);
CREATE INDEX IF NOT EXISTS idx_asset_group_policies_enabled ON asset_group_policies(is_enabled);

-- Tabela de logs de ações em grupos (auditoria)
CREATE TABLE IF NOT EXISTS asset_group_logs (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL,
    action VARCHAR(50) NOT NULL, -- 'created', 'updated', 'asset_added', 'asset_removed', etc
    details TEXT,
    performed_by INTEGER,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_log_group_id FOREIGN KEY (group_id) REFERENCES asset_groups(id) ON DELETE CASCADE
);

-- Índices para asset_group_logs
CREATE INDEX IF NOT EXISTS idx_asset_group_logs_group ON asset_group_logs(group_id);
CREATE INDEX IF NOT EXISTS idx_asset_group_logs_action ON asset_group_logs(action);
CREATE INDEX IF NOT EXISTS idx_asset_group_logs_date ON asset_group_logs(performed_at);

-- Função para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para atualizar updated_at
DROP TRIGGER IF EXISTS update_asset_groups_updated_at ON asset_groups;
CREATE TRIGGER update_asset_groups_updated_at 
    BEFORE UPDATE ON asset_groups 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_asset_group_policies_updated_at ON asset_group_policies;
CREATE TRIGGER update_asset_group_policies_updated_at 
    BEFORE UPDATE ON asset_group_policies 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- View para facilitar consultas de grupos com contagem de assets
CREATE OR REPLACE VIEW v_asset_groups_summary AS
SELECT 
    ag.id,
    ag.name,
    ag.description,
    ag.created_at,
    ag.is_active,
    COUNT(DISTINCT agi.asset_id) as asset_count,
    COUNT(DISTINCT agp.id) as policy_count
FROM asset_groups ag
LEFT JOIN asset_group_items agi ON ag.id = agi.group_id
LEFT JOIN asset_group_policies agp ON ag.id = agp.group_id AND agp.is_enabled = TRUE
GROUP BY ag.id, ag.name, ag.description, ag.created_at, ag.is_active;

-- Inserir alguns dados de exemplo (opcional - descomente se desejar)
-- INSERT INTO asset_groups (name, description) VALUES 
-- ('Notebooks Desenvolvimento', 'Grupo de notebooks do time de desenvolvimento'),
-- ('Desktops Administrativo', 'Computadores do setor administrativo'),
-- ('Servidores Produção', 'Servidores em ambiente de produção');

-- Comentário sobre permissões
-- Certifique-se de que o usuário da aplicação tenha as permissões necessárias:
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO seu_usuario;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO seu_usuario;
-- GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO seu_usuario;
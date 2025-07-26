-- Esquema para Gerenciamento de Software
-- Tabelas para grupos de software, políticas e controle de instalação

-- Tabela de grupos de software
CREATE TABLE software_groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_required BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de itens de software nos grupos
CREATE TABLE software_group_items (
    id SERIAL PRIMARY KEY,
    group_id INTEGER REFERENCES software_groups(id) ON DELETE CASCADE,
    software_name VARCHAR(255) NOT NULL,
    software_vendor VARCHAR(255),
    software_version VARCHAR(100),
    is_required BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(group_id, software_name, software_vendor, software_version)
);

-- Tabela de relacionamento entre grupos de software e assets
CREATE TABLE software_group_assets (
    id SERIAL PRIMARY KEY,
    group_id INTEGER REFERENCES software_groups(id) ON DELETE CASCADE,
    asset_id INTEGER REFERENCES assets(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_by INTEGER REFERENCES users(id),
    UNIQUE(group_id, asset_id)
);

-- Tabela de status de instalação de software
CREATE TABLE software_installation_status (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(id) ON DELETE CASCADE,
    software_name VARCHAR(255) NOT NULL,
    software_vendor VARCHAR(255),
    software_version VARCHAR(100),
    action_type VARCHAR(50) NOT NULL, -- 'install', 'uninstall', 'update'
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'in_progress', 'completed', 'failed', 'blocked'
    error_message TEXT,
    blocked_reason TEXT, -- Motivo do bloqueio se status = 'blocked'
    scheduled_date TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de políticas de software por grupo
CREATE TABLE software_policies (
    id SERIAL PRIMARY KEY,
    group_id INTEGER REFERENCES software_groups(id) ON DELETE CASCADE,
    policy_name VARCHAR(255) NOT NULL,
    policy_type VARCHAR(50) NOT NULL, -- 'installation', 'uninstallation', 'update', 'blocking'
    policy_value TEXT,
    is_enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de logs de execução de software
CREATE TABLE software_execution_logs (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(id) ON DELETE CASCADE,
    software_name VARCHAR(255) NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    execution_status VARCHAR(50) NOT NULL, -- 'success', 'failed', 'blocked'
    execution_message TEXT,
    execution_details JSONB,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    executed_by INTEGER REFERENCES users(id)
);

-- Índices para performance
CREATE INDEX idx_software_groups_name ON software_groups(name);
CREATE INDEX idx_software_group_items_group ON software_group_items(group_id);
CREATE INDEX idx_software_group_assets_group ON software_group_assets(group_id);
CREATE INDEX idx_software_group_assets_asset ON software_group_assets(asset_id);
CREATE INDEX idx_software_installation_status_asset ON software_installation_status(asset_id);
CREATE INDEX idx_software_installation_status_status ON software_installation_status(status);
CREATE INDEX idx_software_policies_group ON software_policies(group_id);
CREATE INDEX idx_software_execution_logs_asset ON software_execution_logs(asset_id);
CREATE INDEX idx_software_execution_logs_executed_at ON software_execution_logs(executed_at);

-- Inserir dados de exemplo
INSERT INTO software_groups (name, description, is_required) VALUES
('Software Básico', 'Software essencial para todos os computadores', true),
('Software de Desenvolvimento', 'Ferramentas de desenvolvimento para programadores', false),
('Software de Segurança', 'Antivírus e ferramentas de segurança', true),
('Software de Produtividade', 'Office e ferramentas de produtividade', false);

-- Inserir itens de software básico
INSERT INTO software_group_items (group_id, software_name, software_vendor, software_version, is_required) VALUES
(1, 'Google Chrome', 'Google LLC', 'latest', true),
(1, 'Mozilla Firefox', 'Mozilla Corporation', 'latest', false),
(1, '7-Zip', 'Igor Pavlov', 'latest', true),
(1, 'Adobe Reader', 'Adobe Inc.', 'latest', true);

-- Inserir itens de software de desenvolvimento
INSERT INTO software_group_items (group_id, software_name, software_vendor, software_version, is_required) VALUES
(2, 'Visual Studio Code', 'Microsoft Corporation', 'latest', true),
(2, 'Git', 'Git for Windows', 'latest', true),
(2, 'Python', 'Python Software Foundation', '3.11', true),
(2, 'Node.js', 'Node.js Foundation', 'latest', false);

-- Inserir itens de software de segurança
INSERT INTO software_group_items (group_id, software_name, software_vendor, software_version, is_required) VALUES
(3, 'Windows Defender', 'Microsoft Corporation', 'latest', true),
(3, 'Malwarebytes', 'Malwarebytes Corporation', 'latest', false);

-- Inserir políticas de exemplo
INSERT INTO software_policies (group_id, policy_name, policy_type, policy_value, is_enabled) VALUES
(1, 'Instalação Automática', 'installation', '{"auto_install": true, "silent_install": true}', true),
(1, 'Bloqueio de Desinstalação', 'blocking', '{"prevent_uninstall": true, "reason": "Software essencial"}', true),
(2, 'Instalação Manual', 'installation', '{"auto_install": false, "require_approval": true}', true),
(3, 'Atualização Automática', 'update', '{"auto_update": true, "check_interval": "daily"}', true); 
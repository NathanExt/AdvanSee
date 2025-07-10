-- Sistema de Gestão de Inventário Automatizado
-- Esquema do Banco de Dados PostgreSQL

-- Tabela de organizações
CREATE TABLE organizations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de usuários
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de categorias de ativos
CREATE TABLE asset_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_id INTEGER REFERENCES asset_categories(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de fornecedores
CREATE TABLE vendors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255),
    contact_phone VARCHAR(50),
    address TEXT,
    website VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de localizações
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    address TEXT,
    building VARCHAR(100),
    floor VARCHAR(50),
    room VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela principal de ativos
CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id),
    asset_tag VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category_id INTEGER REFERENCES asset_categories(id),
    vendor_id INTEGER REFERENCES vendors(id),
    model VARCHAR(255),
    serial_number VARCHAR(255),
    purchase_date DATE,
    purchase_cost DECIMAL(12,2),
    warranty_expiry DATE,
    location_id INTEGER REFERENCES locations(id),
    assigned_user_id INTEGER REFERENCES users(id),
    status VARCHAR(50) DEFAULT 'active',
    criticality VARCHAR(20) DEFAULT 'medium',
    ip_address VARCHAR(45), -- Changed from INET to VARCHAR
    mac_address VARCHAR(17), -- Changed from MACADDR to VARCHAR
    operating_system VARCHAR(255),
    os_version VARCHAR(100),
    python_version VARCHAR(50), -- New column
    architecture VARCHAR(50), -- New column
    processor VARCHAR(255), -- New column
    cpu_count INTEGER, -- New column
    cpu_count_logical INTEGER, -- New column
    cpu_freq_current DECIMAL(10,2), -- New column
    cpu_freq_min DECIMAL(10,2), -- New column
    cpu_freq_max DECIMAL(10,2), -- New column
    total_memory_bytes BIGINT, -- New column
    available_memory_bytes BIGINT, -- New column
    memory_percent DECIMAL(5,2), -- New column
    total_disk_bytes BIGINT, -- New column
    used_disk_bytes BIGINT, -- New column
    free_disk_bytes BIGINT, -- New column
    disk_percent DECIMAL(5,2), -- New column
    disk_model VARCHAR(255), -- New column
    disk_serial VARCHAR(255), -- New column
    disk_interface_type VARCHAR(50), -- New column
    computer_model VARCHAR(255), -- New column for computer model
    computer_manufacturer VARCHAR(255), -- New column for computer manufacturer
    computer_system_type VARCHAR(100), -- New column for system type
    last_seen TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de software instalado
CREATE TABLE software (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    vendor VARCHAR(255),
    version VARCHAR(100),
    license_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Tabela de interfaces de rede (normalized from system_info.network_interfaces)
CREATE TABLE network_interfaces (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    mac_address VARCHAR(17),
    ip_address VARCHAR(45),
    netmask VARCHAR(45),
    broadcast VARCHAR(45),
    family VARCHAR(50), -- To store address family like '2' for IPv4, '23' for IPv6, '-1' for MAC
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de software instalado (normalized from system_info.installed_software)
CREATE TABLE installed_software (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    version VARCHAR(100),
    vendor VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(asset_id, name, version, vendor) -- Added uniqueness constraint
);

-- Tabela de instalações de software
CREATE TABLE asset_software (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(id) ON DELETE CASCADE,
    software_id INTEGER REFERENCES software(id),
    version VARCHAR(100),
    install_date DATE,
    license_key VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(asset_id, software_id)
);

-- Tabela de licenças
CREATE TABLE licenses (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id),
    software_id INTEGER REFERENCES software(id),
    license_key VARCHAR(255),
    license_type VARCHAR(100),
    seats_total INTEGER,
    seats_used INTEGER DEFAULT 0,
    purchase_date DATE,
    expiry_date DATE,
    cost DECIMAL(12,2),
    vendor_id INTEGER REFERENCES vendors(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de vulnerabilidades
CREATE TABLE vulnerabilities (
    id SERIAL PRIMARY KEY,
    cve_id VARCHAR(50) UNIQUE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    severity VARCHAR(20),
    cvss_score DECIMAL(3,1),
    published_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de vulnerabilidades por ativo
CREATE TABLE asset_vulnerabilities (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(id) ON DELETE CASCADE,
    vulnerability_id INTEGER REFERENCES vulnerabilities(id),
    status VARCHAR(50) DEFAULT 'open',
    detected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_date TIMESTAMP,
    notes TEXT,
    UNIQUE(asset_id, vulnerability_id)
);

-- Tabela de patches
CREATE TABLE patches (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    vendor VARCHAR(255),
    patch_id VARCHAR(255),
    release_date DATE,
    severity VARCHAR(20),
    kb_article VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de patches por ativo
CREATE TABLE asset_patches (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(id) ON DELETE CASCADE,
    patch_id INTEGER REFERENCES patches(id),
    status VARCHAR(50) DEFAULT 'pending',
    installed_date TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(asset_id, patch_id)
);

-- Tabela de agentes (original, configuration will store JSON data like running_processes, windows_services, windows_updates)
CREATE TABLE agents (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(id) ON DELETE CASCADE,
    agent_version VARCHAR(50),
    last_checkin TIMESTAMP,
    status VARCHAR(50) DEFAULT 'active',
    configuration JSONB, -- Storing complex, less queried data here
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de histórico de mudanças
CREATE TABLE asset_history (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    field_name VARCHAR(100),
    old_value TEXT,
    new_value TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de relatórios de descoberta (original, no change)
CREATE TABLE discovery_reports (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id),
    scan_type VARCHAR(100),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    assets_discovered INTEGER DEFAULT 0,
    assets_updated INTEGER DEFAULT 0,
    status VARCHAR(50),
    report_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de atualizações do Windows (normalized from system_info.windows_updates)
CREATE TABLE windows_updates (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(id) ON DELETE CASCADE,
    hotfix_id VARCHAR(100) NOT NULL,
    description TEXT,
    installed_on DATE,
    installed_by VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(asset_id, hotfix_id)
);


-- Índices para performance
CREATE INDEX idx_assets_organization ON assets(organization_id);
CREATE INDEX idx_assets_category ON assets(category_id);
CREATE INDEX idx_assets_location ON assets(location_id);
CREATE INDEX idx_assets_status ON assets(status);
CREATE INDEX idx_assets_ip ON assets(ip_address);
CREATE INDEX idx_asset_software_asset ON installed_software(asset_id); -- Index changed to new table
CREATE INDEX idx_asset_vulnerabilities_asset ON asset_vulnerabilities(asset_id);
CREATE INDEX idx_asset_patches_asset ON asset_patches(asset_id);
CREATE INDEX idx_agents_asset ON agents(asset_id);
CREATE INDEX idx_asset_history_asset ON asset_history(asset_id);
CREATE INDEX idx_network_interfaces_asset ON network_interfaces(asset_id); -- New index
CREATE INDEX idx_windows_updates_asset ON windows_updates(asset_id); -- New index
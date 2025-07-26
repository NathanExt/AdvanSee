-- Sistema de Gestão de Inventário Automatizado
-- Esquema do Banco de Dados PostgreSQL - Versão Otimizada


-- Tabela de usuários de ativos (proprietários/responsáveis)
CREATE TABLE asset_usuario (
    usuario_id SERIAL PRIMARY KEY,
    usuario_nome VARCHAR(255) NOT NULL,
    usuario_email VARCHAR(255) UNIQUE NOT NULL,
    usuario_ou VARCHAR(255),
    usuario_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de categorias (reutilizável para múltiplos ativos)
CREATE TABLE asset_categoria (
    categoria_id SERIAL PRIMARY KEY,
    categoria_name VARCHAR(255) UNIQUE NOT NULL,
    categoria_description TEXT,
    categoria_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela principal de ativos
CREATE TABLE asset_tabela_principal(
    asset_id SERIAL PRIMARY KEY,
    asset_tag VARCHAR(255) UNIQUE NOT NULL,
    asset_hostname VARCHAR(255) NOT NULL,
    asset_description TEXT,
    asset_num_serial VARCHAR(255),
    asset_modelo VARCHAR(255),
    asset_fabricante VARCHAR(255),
    asset_tipo_sistema VARCHAR(50),
    asset_num_serie VARCHAR(255),
    asset_service_tag VARCHAR(150) UNIQUE NOT NULL,
    asset_so VARCHAR(255),
    asset_status VARCHAR(50),


    -- Relacionamentos
    asset_id_usuario INTEGER REFERENCES asset_usuario(usuario_id) ON DELETE SET NULL,
    asset_id_category INTEGER REFERENCES asset_categoria(categoria_id) ON DELETE SET NULL,

    asset_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    asset_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Componentes específicos de cada ativo (1:1 com asset)
-- ASSET CPU (cada ativo tem sua própria CPU)
CREATE TABLE asset_cpu(
    cpu_id SERIAL PRIMARY KEY,
    asset_id INTEGER UNIQUE NOT NULL REFERENCES asset_tabela_principal(asset_id) ON DELETE CASCADE,
    cpu_processor VARCHAR(255),
    cpu_count INTEGER,
    cpu_count_logical INTEGER,
    cpu_freq_current DECIMAL(10,2),
    cpu_freq_min DECIMAL(10,2),
    cpu_freq_max DECIMAL(10,2),
    cpu_architecture VARCHAR(50),
    cpu_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cpu_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ASSET MEMÓRIA (cada ativo tem sua própria memória)
CREATE TABLE asset_memoria(
    memoria_id SERIAL PRIMARY KEY,
    asset_id INTEGER UNIQUE NOT NULL REFERENCES asset_tabela_principal(asset_id) ON DELETE CASCADE,
    memoria_total BIGINT,
    memoria_available BIGINT,
    memoria_used BIGINT,
    memoria_percent DECIMAL(5,2),
    memoria_type VARCHAR(50), -- DDR3, DDR4, DDR5
    memoria_speed INTEGER, -- MHz
    memoria_slots_total INTEGER,
    memoria_slots_used INTEGER,
    memoria_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    memoria_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ASSET DISCO (um ativo pode ter múltiplos discos)
CREATE TABLE asset_disco(
    disco_id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES asset_tabela_principal(asset_id) ON DELETE CASCADE,
    disco_device VARCHAR(255), -- /dev/sda, C:, etc
    disco_mount_point VARCHAR(255), -- /, C:\, /home, etc
    disco_total BIGINT,
    disco_used BIGINT,
    disco_free BIGINT,
    disco_percent DECIMAL(5,2),
    disco_model VARCHAR(255),
    disco_serial VARCHAR(255),
    disco_interface_type VARCHAR(50), -- SATA, NVMe, SAS
    disco_type VARCHAR(50), -- SSD, HDD
    disco_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    disco_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ASSET GPU (um ativo pode ter múltiplas GPUs)
CREATE TABLE asset_gpu(
    gpu_id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES asset_tabela_principal(asset_id) ON DELETE CASCADE,
    gpu_name VARCHAR(255) NOT NULL,
    gpu_vendor VARCHAR(255),
    gpu_memory BIGINT,
    gpu_driver_version VARCHAR(100),
    gpu_index INTEGER DEFAULT 0, -- Para múltiplas GPUs
    gpu_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    gpu_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ASSET INTERFACES DE REDE (um ativo pode ter múltiplas interfaces)
CREATE TABLE asset_network_interfaces(
    interface_id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES asset_tabela_principal(asset_id) ON DELETE CASCADE,
    interface_name VARCHAR(255),
    interface_mac_address VARCHAR(17),
    interface_ip_address VARCHAR(45),
    interface_netmask VARCHAR(45),
    interface_gateway VARCHAR(45),
    interface_speed BIGINT,
    interface_status VARCHAR(50),
    interface_type VARCHAR(50), -- Ethernet, WiFi, etc
    interface_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    interface_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SOFTWARE instalado (um ativo pode ter múltiplos softwares)
CREATE TABLE asset_software(
    software_id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES asset_tabela_principal(asset_id) ON DELETE CASCADE,
    software_name VARCHAR(255) NOT NULL,
    software_fabricante VARCHAR(255),
    software_version VARCHAR(100),
    software_install_date DATE,
    software_license_key VARCHAR(255),
    software_license_type VARCHAR(100),
    software_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    software_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PROCESSOS em execução (snapshot temporal)
CREATE TABLE asset_processo(
    processo_id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES asset_tabela_principal(asset_id) ON DELETE CASCADE,
    processo_name VARCHAR(255) NOT NULL,
    processo_pid INTEGER NOT NULL,
    processo_user VARCHAR(255),
    processo_memory_usage BIGINT,
    processo_cpu_usage DECIMAL(5,2),
    processo_start_time TIMESTAMP,
    processo_status VARCHAR(50),
    processo_command_line TEXT,
    processo_snapshot_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DESEMPENHO (histórico temporal)
CREATE TABLE asset_desempenho(
    desempenho_id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES asset_tabela_principal(asset_id) ON DELETE CASCADE,
    desempenho_cpu_usage DECIMAL(5,2),
    desempenho_memory_usage BIGINT,
    desempenho_memory_percent DECIMAL(5,2),
    desempenho_disk_read_bytes BIGINT,
    desempenho_disk_write_bytes BIGINT,
    desempenho_network_sent_bytes BIGINT,
    desempenho_network_recv_bytes BIGINT,
    desempenho_gpu_usage DECIMAL(5,2),
    desempenho_temperature_cpu DECIMAL(5,2),
    desempenho_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SERVIÇOS do sistema (um ativo pode ter múltiplos serviços)
CREATE TABLE asset_service(
    service_id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES asset_tabela_principal(asset_id) ON DELETE CASCADE,
    service_name VARCHAR(255) NOT NULL,
    service_display_name VARCHAR(255),
    service_status VARCHAR(50) NOT NULL,
    service_start_type VARCHAR(50),
    service_description TEXT,
    service_path VARCHAR(500),
    service_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    service_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- HISTÓRICO de mudanças (auditoria)
CREATE TABLE asset_historico(
    historico_id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES asset_tabela_principal(asset_id) ON DELETE CASCADE,
    historico_action VARCHAR(50) NOT NULL, -- CREATE, UPDATE, DELETE, STATUS_CHANGE
    historico_field_name VARCHAR(100),
    historico_old_value TEXT,
    historico_new_value TEXT,
    historico_description TEXT,
    historico_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Índices para performance
-- Índices para tabela principal
CREATE INDEX idx_asset_tag ON asset_tabela_principal(asset_tag);
CREATE INDEX idx_asset_hostname ON asset_tabela_principal(asset_hostname);
CREATE INDEX idx_asset_service_tag ON asset_tabela_principal(asset_service_tag);
CREATE INDEX idx_asset_status ON asset_tabela_principal(asset_status);
CREATE INDEX idx_asset_usuario ON asset_tabela_principal(asset_id_usuario);
CREATE INDEX idx_asset_category ON asset_tabela_principal(asset_id_category);

-- Índices para tabelas relacionadas
CREATE INDEX idx_disco_asset ON asset_disco(asset_id);

CREATE INDEX idx_gpu_asset ON asset_gpu(asset_id);
CREATE INDEX idx_network_ip ON asset_network_interfaces(interface_ip_address);
CREATE INDEX idx_network_asset ON asset_network_interfaces(asset_id);
CREATE INDEX idx_network_mac ON asset_network_interfaces(interface_mac_address);

CREATE INDEX idx_software_asset ON asset_software(asset_id);
CREATE INDEX idx_software_name ON asset_software(software_name);

CREATE INDEX idx_processo_asset ON asset_processo(asset_id, processo_snapshot_time);
CREATE INDEX idx_processo_pid ON asset_processo(processo_pid);

CREATE INDEX idx_desempenho_asset ON asset_desempenho(asset_id, desempenho_timestamp);

CREATE INDEX idx_service_asset ON asset_service(asset_id);
CREATE INDEX idx_service_name ON asset_service(service_name);
CREATE INDEX idx_service_status ON asset_service(service_status);

CREATE INDEX idx_historico_asset ON asset_historico(asset_id, historico_timestamp);
CREATE INDEX idx_historico_action ON asset_historico(historico_action);


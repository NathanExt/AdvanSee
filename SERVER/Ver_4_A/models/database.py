"""
Modelos SQLAlchemy para Sistema de Gestão de Inventário Automatizado
Compatível com Flask-SQLAlchemy
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index, event
from sqlalchemy.orm import validates

db = SQLAlchemy()


class AssetUsuario(db.Model):
    """Modelo para usuários responsáveis pelos ativos"""
    __tablename__ = 'asset_usuario'

    usuario_id = db.Column(db.Integer, primary_key=True)
    usuario_nome = db.Column(db.String(255), nullable=False)
    usuario_email = db.Column(db.String(255), unique=True, nullable=False)
    usuario_ou = db.Column(db.String(255))
    usuario_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    assets = db.relationship('AssetTabelaPrincipal', back_populates='usuario', lazy='dynamic')

    def __repr__(self):
        return f'<AssetUsuario {self.usuario_nome}>'

    @validates('usuario_email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("Email inválido")
        return email.lower()


class AssetCategoria(db.Model):
    """Modelo para categorias de ativos"""
    __tablename__ = 'asset_categoria'

    categoria_id = db.Column(db.Integer, primary_key=True)
    categoria_name = db.Column(db.String(255), unique=True, nullable=False)
    categoria_description = db.Column(db.Text)
    categoria_created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    assets = db.relationship('AssetTabelaPrincipal', back_populates='categoria', lazy='dynamic')

    def __repr__(self):
        return f'<AssetCategoria {self.categoria_name}>'


class AssetTabelaPrincipal(db.Model):
    """Modelo principal para ativos"""
    __tablename__ = 'asset_tabela_principal'

    asset_id = db.Column(db.Integer, primary_key=True)
    asset_tag = db.Column(db.String(255), unique=True, nullable=False, index=True)
    asset_hostname = db.Column(db.String(255), nullable=False, index=True)
    asset_description = db.Column(db.Text)
    asset_num_serial = db.Column(db.String(255))
    asset_modelo = db.Column(db.String(255))
    asset_fabricante = db.Column(db.String(255))
    asset_tipo_sistema = db.Column(db.String(50))
    asset_num_serie = db.Column(db.String(255))
    asset_service_tag = db.Column(db.String(150), unique=True, nullable=False, index=True)
    asset_so = db.Column(db.String(255))
    asset_status = db.Column(db.String(50), default='Ativo', index=True)

    # Chaves estrangeiras
    asset_id_usuario = db.Column(db.Integer, db.ForeignKey('asset_usuario.usuario_id', ondelete='SET NULL'))
    asset_id_category = db.Column(db.Integer, db.ForeignKey('asset_categoria.categoria_id', ondelete='SET NULL'))

    # Timestamps
    asset_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    asset_updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    usuario = db.relationship('AssetUsuario', back_populates='assets')
    categoria = db.relationship('AssetCategoria', back_populates='assets')
    cpu = db.relationship('AssetCpu', back_populates='asset', uselist=False, cascade='all, delete-orphan')
    memoria = db.relationship('AssetMemoria', back_populates='asset', uselist=False, cascade='all, delete-orphan')
    discos = db.relationship('AssetDisco', back_populates='asset', cascade='all, delete-orphan')
    gpus = db.relationship('AssetGpu', back_populates='asset', cascade='all, delete-orphan')
    network_interfaces = db.relationship('AssetNetworkInterface', back_populates='asset', cascade='all, delete-orphan')
    softwares = db.relationship('AssetSoftware', back_populates='asset', cascade='all, delete-orphan')
    processos = db.relationship('AssetProcesso', back_populates='asset', cascade='all, delete-orphan')
    desempenhos = db.relationship('AssetDesempenho', back_populates='asset', cascade='all, delete-orphan')
    servicos = db.relationship('AssetService', back_populates='asset', cascade='all, delete-orphan')
    historicos = db.relationship('AssetHistorico', back_populates='asset', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Asset {self.asset_hostname} - {self.asset_tag}>'

    @property
    def is_active(self):
        return self.asset_status == 'Ativo'

    def add_historico(self, action, field_name=None, old_value=None, new_value=None, description=None):
        """Adiciona entrada no histórico do ativo"""
        historico = AssetHistorico(
            asset_id=self.asset_id,
            historico_action=action,
            historico_field_name=field_name,
            historico_old_value=str(old_value) if old_value else None,
            historico_new_value=str(new_value) if new_value else None,
            historico_description=description
        )
        db.session.add(historico)
        return historico


class AssetCpu(db.Model):
    """Modelo para informações de CPU"""
    __tablename__ = 'asset_cpu'

    cpu_id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset_tabela_principal.asset_id', ondelete='CASCADE'),
                         unique=True, nullable=False)
    cpu_processor = db.Column(db.String(255))
    cpu_count = db.Column(db.Integer)
    cpu_count_logical = db.Column(db.Integer)
    cpu_freq_current = db.Column(db.Numeric(10, 2))
    cpu_freq_min = db.Column(db.Numeric(10, 2))
    cpu_freq_max = db.Column(db.Numeric(10, 2))
    cpu_architecture = db.Column(db.String(50))
    cpu_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    cpu_updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    asset = db.relationship('AssetTabelaPrincipal', back_populates='cpu')

    def __repr__(self):
        return f'<AssetCpu {self.cpu_processor}>'


class AssetMemoria(db.Model):
    """Modelo para informações de memória"""
    __tablename__ = 'asset_memoria'

    memoria_id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset_tabela_principal.asset_id', ondelete='CASCADE'),
                         unique=True, nullable=False)
    memoria_total = db.Column(db.BigInteger)
    memoria_available = db.Column(db.BigInteger)
    memoria_used = db.Column(db.BigInteger)
    memoria_percent = db.Column(db.Numeric(5, 2))
    memoria_type = db.Column(db.String(50))
    memoria_speed = db.Column(db.Integer)
    memoria_slots_total = db.Column(db.Integer)
    memoria_slots_used = db.Column(db.Integer)
    memoria_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    memoria_updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    asset = db.relationship('AssetTabelaPrincipal', back_populates='memoria')

    def __repr__(self):
        return f'<AssetMemoria {self.memoria_total}>'

    @property
    def memoria_total_gb(self):
        """Retorna memória total em GB"""
        return round(self.memoria_total / (1024 ** 3), 2) if self.memoria_total else 0


class AssetDisco(db.Model):
    """Modelo para informações de disco"""
    __tablename__ = 'asset_disco'

    disco_id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset_tabela_principal.asset_id', ondelete='CASCADE'),
                         nullable=False, index=True)
    disco_device = db.Column(db.String(255))
    disco_mount_point = db.Column(db.String(255))
    disco_total = db.Column(db.BigInteger)
    disco_used = db.Column(db.BigInteger)
    disco_free = db.Column(db.BigInteger)
    disco_percent = db.Column(db.Numeric(5, 2))
    disco_model = db.Column(db.String(255))
    disco_serial = db.Column(db.String(255))
    disco_interface_type = db.Column(db.String(50))
    disco_type = db.Column(db.String(50))
    disco_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    disco_updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    asset = db.relationship('AssetTabelaPrincipal', back_populates='discos')

    def __repr__(self):
        return f'<AssetDisco {self.disco_device} - {self.disco_mount_point}>'

    @property
    def disco_total_gb(self):
        """Retorna espaço total em GB"""
        return round(self.disco_total / (1024 ** 3), 2) if self.disco_total else 0

    @property
    def disco_used_gb(self):
        """Retorna espaço usado em GB"""
        return round(self.disco_used / (1024 ** 3), 2) if self.disco_used else 0


class AssetGpu(db.Model):
    """Modelo para informações de GPU"""
    __tablename__ = 'asset_gpu'

    gpu_id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset_tabela_principal.asset_id', ondelete='CASCADE'),
                         nullable=False, index=True)
    gpu_name = db.Column(db.String(255), nullable=False)
    gpu_vendor = db.Column(db.String(255))
    gpu_memory = db.Column(db.BigInteger)
    gpu_driver_version = db.Column(db.String(100))
    gpu_index = db.Column(db.Integer, default=0)
    gpu_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    gpu_updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    asset = db.relationship('AssetTabelaPrincipal', back_populates='gpus')

    def __repr__(self):
        return f'<AssetGpu {self.gpu_name}>'


class AssetNetworkInterface(db.Model):
    """Modelo para interfaces de rede"""
    __tablename__ = 'asset_network_interfaces'

    interface_id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset_tabela_principal.asset_id', ondelete='CASCADE'),
                         nullable=False, index=True)
    interface_name = db.Column(db.String(255))
    interface_mac_address = db.Column(db.String(17), index=True)
    interface_ip_address = db.Column(db.String(45), index=True)
    interface_netmask = db.Column(db.String(45))
    interface_gateway = db.Column(db.String(45))
    interface_speed = db.Column(db.BigInteger)
    interface_status = db.Column(db.String(50))
    interface_type = db.Column(db.String(50))
    interface_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    interface_updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    asset = db.relationship('AssetTabelaPrincipal', back_populates='network_interfaces')

    def __repr__(self):
        return f'<AssetNetworkInterface {self.interface_name} - {self.interface_ip_address}>'


class AssetSoftware(db.Model):
    """Modelo para software instalado"""
    __tablename__ = 'asset_software'

    software_id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset_tabela_principal.asset_id', ondelete='CASCADE'),
                         nullable=False, index=True)
    software_name = db.Column(db.String(255), nullable=False, index=True)
    software_fabricante = db.Column(db.String(255))
    software_version = db.Column(db.String(100))
    software_install_date = db.Column(db.Date)
    software_license_key = db.Column(db.String(255))
    software_license_type = db.Column(db.String(100))
    software_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    software_updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    asset = db.relationship('AssetTabelaPrincipal', back_populates='softwares')

    def __repr__(self):
        return f'<AssetSoftware {self.software_name} v{self.software_version}>'


class AssetProcesso(db.Model):
    """Modelo para processos em execução"""
    __tablename__ = 'asset_processo'

    processo_id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset_tabela_principal.asset_id', ondelete='CASCADE'),
                         nullable=False)
    processo_name = db.Column(db.String(255), nullable=False)
    processo_pid = db.Column(db.Integer, nullable=False, index=True)
    processo_user = db.Column(db.String(255))
    processo_memory_usage = db.Column(db.BigInteger)
    processo_cpu_usage = db.Column(db.Numeric(5, 2))
    processo_start_time = db.Column(db.DateTime)
    processo_status = db.Column(db.String(50))
    processo_command_line = db.Column(db.Text)
    processo_snapshot_time = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    asset = db.relationship('AssetTabelaPrincipal', back_populates='processos')

    # Índice composto
    __table_args__ = (
        Index('idx_processo_asset', 'asset_id', 'processo_snapshot_time'),
    )

    def __repr__(self):
        return f'<AssetProcesso {self.processo_name} PID:{self.processo_pid}>'


class AssetDesempenho(db.Model):
    """Modelo para métricas de desempenho"""
    __tablename__ = 'asset_desempenho'

    desempenho_id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset_tabela_principal.asset_id', ondelete='CASCADE'),
                         nullable=False)
    desempenho_cpu_usage = db.Column(db.Numeric(5, 2))
    desempenho_memory_usage = db.Column(db.BigInteger)
    desempenho_memory_percent = db.Column(db.Numeric(5, 2))
    desempenho_disk_read_bytes = db.Column(db.BigInteger)
    desempenho_disk_write_bytes = db.Column(db.BigInteger)
    desempenho_network_sent_bytes = db.Column(db.BigInteger)
    desempenho_network_recv_bytes = db.Column(db.BigInteger)
    desempenho_gpu_usage = db.Column(db.Numeric(5, 2))
    desempenho_temperature_cpu = db.Column(db.Numeric(5, 2))
    desempenho_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    asset = db.relationship('AssetTabelaPrincipal', back_populates='desempenhos')

    # Índice composto
    __table_args__ = (
        Index('idx_desempenho_asset', 'asset_id', 'desempenho_timestamp'),
    )

    def __repr__(self):
        return f'<AssetDesempenho Asset:{self.asset_id} Time:{self.desempenho_timestamp}>'


class AssetService(db.Model):
    """Modelo para serviços do sistema"""
    __tablename__ = 'asset_service'

    service_id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset_tabela_principal.asset_id', ondelete='CASCADE'),
                         nullable=False, index=True)
    service_name = db.Column(db.String(255), nullable=False, index=True)
    service_display_name = db.Column(db.String(255))
    service_status = db.Column(db.String(50), nullable=False, index=True)
    service_start_type = db.Column(db.String(50))
    service_description = db.Column(db.Text)
    service_path = db.Column(db.String(500))
    service_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    service_updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    asset = db.relationship('AssetTabelaPrincipal', back_populates='servicos')

    def __repr__(self):
        return f'<AssetService {self.service_name} - {self.service_status}>'


class AssetHistorico(db.Model):
    """Modelo para histórico de mudanças"""
    __tablename__ = 'asset_historico'

    historico_id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset_tabela_principal.asset_id', ondelete='CASCADE'),
                         nullable=False)
    historico_action = db.Column(db.String(50), nullable=False, index=True)
    historico_field_name = db.Column(db.String(100))
    historico_old_value = db.Column(db.Text)
    historico_new_value = db.Column(db.Text)
    historico_description = db.Column(db.Text)
    historico_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    asset = db.relationship('AssetTabelaPrincipal', back_populates='historicos')

    # Índice composto
    __table_args__ = (
        Index('idx_historico_asset', 'asset_id', 'historico_timestamp'),
    )

    def __repr__(self):
        return f'<AssetHistorico {self.historico_action} Asset:{self.asset_id}>'


# Event listeners para atualização automática de timestamps
@event.listens_for(AssetUsuario, 'before_update')
@event.listens_for(AssetTabelaPrincipal, 'before_update')
@event.listens_for(AssetCpu, 'before_update')
@event.listens_for(AssetMemoria, 'before_update')
@event.listens_for(AssetDisco, 'before_update')
@event.listens_for(AssetGpu, 'before_update')
@event.listens_for(AssetNetworkInterface, 'before_update')
@event.listens_for(AssetSoftware, 'before_update')
@event.listens_for(AssetService, 'before_update')
def update_timestamp(mapper, connection, target):
    """Atualiza timestamp automaticamente antes de update"""
    if hasattr(target, 'updated_at'):
        target.updated_at = datetime.utcnow()
    elif hasattr(target, f'{target.__tablename__.split("_")[1]}_updated_at'):
        setattr(target, f'{target.__tablename__.split("_")[1]}_updated_at', datetime.utcnow())




# Funções auxiliares para queries comuns
class AssetQueries:
    """Classe com queries úteis para o sistema"""

    @staticmethod
    def get_active_assets():
        """Retorna todos os ativos com status 'Ativo'"""
        return AssetTabelaPrincipal.query.filter_by(asset_status='Ativo').all()

    @staticmethod
    def get_assets_by_usuario(usuario_id):
        """Retorna todos os ativos de um usuário"""
        return AssetTabelaPrincipal.query.filter_by(asset_id_usuario=usuario_id).all()

    @staticmethod
    def get_assets_by_categoria(categoria_id):
        """Retorna todos os ativos de uma categoria"""
        return AssetTabelaPrincipal.query.filter_by(asset_id_category=categoria_id).all()

    @staticmethod
    def get_asset_with_components(asset_id):
        """Retorna um ativo com todos seus componentes carregados"""
        return AssetTabelaPrincipal.query.options(
            db.joinedload(AssetTabelaPrincipal.cpu),
            db.joinedload(AssetTabelaPrincipal.memoria),
            db.joinedload(AssetTabelaPrincipal.discos),
            db.joinedload(AssetTabelaPrincipal.gpus),
            db.joinedload(AssetTabelaPrincipal.network_interfaces)
        ).filter_by(asset_id=asset_id).first()

    @staticmethod
    def get_latest_performance(asset_id, limit=10):
        """Retorna as últimas métricas de desempenho de um ativo"""
        return AssetDesempenho.query.filter_by(asset_id=asset_id) \
            .order_by(AssetDesempenho.desempenho_timestamp.desc()) \
            .limit(limit).all()

    @staticmethod
    def search_assets(search_term):
        """Busca ativos por hostname, tag ou service tag"""
        search = f"%{search_term}%"
        return AssetTabelaPrincipal.query.filter(
            db.or_(
                AssetTabelaPrincipal.asset_hostname.ilike(search),
                AssetTabelaPrincipal.asset_tag.ilike(search),
                AssetTabelaPrincipal.asset_service_tag.ilike(search)
            )
        ).all()
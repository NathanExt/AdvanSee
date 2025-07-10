from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Organization(db.Model):
    __tablename__ = 'organizations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    users = db.relationship('User', backref='organization', lazy=True)
    assets = db.relationship('Asset', backref='organization', lazy=True)
    locations = db.relationship('Location', backref='organization', lazy=True)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    role = db.Column(db.String(50), default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AssetCategory(db.Model):
    __tablename__ = 'asset_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('asset_categories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    children = db.relationship('AssetCategory', backref=db.backref('parent', remote_side=[id]))
    assets = db.relationship('Asset', backref='category', lazy=True)

class Vendor(db.Model):
    __tablename__ = 'vendors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(50))
    address = db.Column(db.Text)
    website = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Location(db.Model):
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text)
    building = db.Column(db.String(100))
    floor = db.Column(db.String(50))
    room = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Asset(db.Model):
    __tablename__ = 'assets'
    
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    asset_tag = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('asset_categories.id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    model = db.Column(db.String(255))
    serial_number = db.Column(db.String(255))
    purchase_date = db.Column(db.Date)
    purchase_cost = db.Column(db.Numeric(12, 2))
    warranty_expiry = db.Column(db.Date)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(50), default='active')
    criticality = db.Column(db.String(20), default='medium')
    
    # System Info fields
    ip_address = db.Column(db.String(45)) # Changed from INET
    mac_address = db.Column(db.String(17)) # Changed from MACADDR
    operating_system = db.Column(db.String(255))
    os_version = db.Column(db.String(100))
    python_version = db.Column(db.String(50))
    architecture = db.Column(db.String(50))
    processor = db.Column(db.String(255))
    cpu_count = db.Column(db.Integer)
    cpu_count_logical = db.Column(db.Integer)
    cpu_freq_current = db.Column(db.Numeric(10, 2))
    cpu_freq_min = db.Column(db.Numeric(10, 2))
    cpu_freq_max = db.Column(db.Numeric(10, 2))
    total_memory_bytes = db.Column(db.BigInteger)
    available_memory_bytes = db.Column(db.BigInteger)
    memory_percent = db.Column(db.Numeric(5, 2))
    total_disk_bytes = db.Column(db.BigInteger)
    used_disk_bytes = db.Column(db.BigInteger)
    free_disk_bytes = db.Column(db.BigInteger)
    disk_percent = db.Column(db.Numeric(5, 2))
    disk_model = db.Column(db.String(255))
    disk_serial = db.Column(db.String(255))
    disk_interface_type = db.Column(db.String(50))
    computer_model = db.Column(db.String(255))
    computer_manufacturer = db.Column(db.String(255))
    computer_system_type = db.Column(db.String(100))

    last_seen = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    vendor = db.relationship('Vendor', backref='assets')
    location = db.relationship('Location', backref='assets')
    assigned_user = db.relationship('User', backref='assigned_assets')
    vulnerabilities = db.relationship('AssetVulnerability', backref='asset', lazy=True)
    patches = db.relationship('AssetPatch', backref='asset', lazy=True)
    installed_software_entries = db.relationship('InstalledSoftware', backref='asset', lazy=True, cascade="all, delete-orphan") # Renamed from 'software' to avoid conflict
    network_interfaces_entries = db.relationship('NetworkInterface', backref='asset', lazy=True, cascade="all, delete-orphan")
    windows_updates_entries = db.relationship('WindowsUpdate', backref='asset', lazy=True, cascade="all, delete-orphan")


class InstalledSoftware(db.Model):
    __tablename__ = 'installed_software'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id', ondelete='CASCADE'))
    name = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(100))
    vendor = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('asset_id', 'name', 'version', 'vendor', name='_asset_software_uc'),)


class NetworkInterface(db.Model):
    __tablename__ = 'network_interfaces'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id', ondelete='CASCADE'))
    name = db.Column(db.String(255), nullable=False)
    mac_address = db.Column(db.String(17))
    ip_address = db.Column(db.String(45))
    netmask = db.Column(db.String(45))
    broadcast = db.Column(db.String(45))
    family = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WindowsUpdate(db.Model):
    __tablename__ = 'windows_updates'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id', ondelete='CASCADE'))
    hotfix_id = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    installed_on = db.Column(db.Date)
    installed_by = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('asset_id', 'hotfix_id', name='_asset_hotfix_uc'),)


# Removed the original Software and AssetSoftware models as they are replaced by InstalledSoftware
# If Software and AssetSoftware are used for managing *licensed* software rather than *installed* software,
# they should be kept. Assuming 'installed_software' in the log refers to what was previously intended for
# AssetSoftware, I've created a dedicated table for installed software.

class Software(db.Model): # Keeping if this is for defining software products, not instances
    __tablename__ = 'software'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    vendor = db.Column(db.String(255))
    version = db.Column(db.String(100))
    license_type = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AssetSoftware(db.Model): # Keeping if this is for linking assets to *software products*, not instances
    __tablename__ = 'asset_software'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id', ondelete='CASCADE'))
    software_id = db.Column(db.Integer, db.ForeignKey('software.id'))
    version = db.Column(db.String(100))
    install_date = db.Column(db.Date)
    license_key = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    software = db.relationship('Software', backref='installations')


class Vulnerability(db.Model):
    __tablename__ = 'vulnerabilities'
    
    id = db.Column(db.Integer, primary_key=True)
    cve_id = db.Column(db.String(50), unique=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    severity = db.Column(db.String(20))
    cvss_score = db.Column(db.Numeric(3, 1))
    published_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AssetVulnerability(db.Model):
    __tablename__ = 'asset_vulnerabilities'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id', ondelete='CASCADE'))
    vulnerability_id = db.Column(db.Integer, db.ForeignKey('vulnerabilities.id'))
    status = db.Column(db.String(50), default='open')
    detected_date = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    vulnerability = db.relationship('Vulnerability', backref='asset_vulnerabilities')

class Patch(db.Model):
    __tablename__ = 'patches'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    vendor = db.Column(db.String(255))
    patch_id = db.Column(db.String(255))
    release_date = db.Column(db.Date)
    severity = db.Column(db.String(20))
    kb_article = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AssetPatch(db.Model):
    __tablename__ = 'asset_patches'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id', ondelete='CASCADE'))
    patch_id = db.Column(db.Integer, db.ForeignKey('patches.id'))
    status = db.Column(db.String(50), default='pending')
    installed_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    patch = db.relationship('Patch', backref='asset_patches')

class Agent(db.Model):
    __tablename__ = 'agents'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id', ondelete='CASCADE'))
    agent_version = db.Column(db.String(50))
    last_checkin = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='active')
    configuration = db.Column(db.JSON) # JSONB for PostgreSQL
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AssetHistory(db.Model):
    __tablename__ = 'asset_history'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100), nullable=False)
    field_name = db.Column(db.String(100))
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='asset_changes')
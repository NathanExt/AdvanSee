# config.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

class CONFIG:
    # Configurações gerais
    CAMINHO_LOG = os.path.relpath(os.path.expanduser('~/logs'))
    JWT_SECRET_KEY = 'dIjDw9YncsLcT8ZpBPkL1bl6Yhm7uijnhrwUEg'
    SECRET_KEY = "inventory-system-production-secret-key-2024-ALTERE-ESTA-CHAVE"
    ENCRYPTION_KEY = b'Xexalh4dXCIzMeilnbXok34y5Jx_J5DRP9lR98Yx0rc='
    AGENT_LISTEN_PORT = 60000
    
    # Configurações do banco principal (ISAC)
    DB_HOST = "127.0.0.1"
    DB_USER = "isac"
    DB_PASSWORD = "kwa44fgjc8suf91kjsacaz"
    DB_PORT = "5432"
    
    # Banco principal - ISAC
    DB_NAME_DEFAULT = "ISAC_BD_ADVANSEE_2"
    DATABASE_URL_DEFAULT = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_DEFAULT}"
    )
    
    # Banco PMOC
    DB_NAME_PMOC = "BD_PMOC"
    DATABASE_URL_PMOC = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_PMOC}"
    )
    
    # Configurações SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuração de múltiplos bancos
    SQLALCHEMY_BINDS = {
        'pmoc': DATABASE_URL_PMOC
    }
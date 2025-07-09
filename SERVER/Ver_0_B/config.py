# config.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
class Config:

    CAMINHO_LOG = os.path.relpath(os.path.expanduser('~/logs'))

    DB_HOST = "127.0.0.1"
    DB_NAME = "ISAC_BD_ADVANSEE_2"
    DB_USER = "isac"
    EMAIL = "isac.admin@advansee.com.br"
    DB_PASSWORD = "kwa44fgjc8suf91kjsacaz"
    DB_PORT = "5432"
    JWT_SECRET_KEY = 'dIjDw9YncsLcT8ZpBPkL1bl6Yhm7uijnhrwUEg'
    SECRET_KEY="inventory-system-production-secret-key-2024-ALTERE-ESTA-CHAVE"
    ENCRYPTION_KEY = b'Xexalh4dXCIzMeilnbXok34y5Jx_J5DRP9lR98Yx0rc='
    AGENT_LISTEN_PORT = 60000 
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
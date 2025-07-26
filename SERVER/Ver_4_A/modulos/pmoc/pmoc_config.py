from config import CONFIG

class CONFIG_PMOC:
    # Usar configurações da classe principal
    DB_HOST = CONFIG.DB_HOST
    DB_NAME = CONFIG.DB_NAME_PMOC
    DB_USER = CONFIG.DB_USER
    DB_PASSWORD = CONFIG.DB_PASSWORD
    DB_PORT = CONFIG.DB_PORT
    EMAIL = "isac.admin@advansee.com.br"
    
    # URL do banco PMOC
    DATABASE_URL_PMOC = CONFIG.DATABASE_URL_PMOC
    
    
    # Configurações SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = CONFIG.SQLALCHEMY_TRACK_MODIFICATIONS
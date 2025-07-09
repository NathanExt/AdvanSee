class CONFIG_PMOC:
    DB_HOST = "172.16.0.17"
    DB_NAME = "DB_PMOC"
    DB_USER = "isac"
    EMAIL = "isac.admin@advansee.com.br"
    DB_PASSWORD = "kwa44fgjc8suf91kjsacaz"
    DB_PORT = "5432"
    DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
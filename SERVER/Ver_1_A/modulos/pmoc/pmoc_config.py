class CONFIG_PMOC:
    DB_HOST = "127.0.0.1"
    DB_NAME = "BD_PMOC"
    DB_USER = "isac"
    EMAIL = "isac.admin@advansee.com.br"
    DB_PASSWORD = "kwa44fgjc8suf91kjsacaz"
    DB_PORT = "5432"
    DATABASE_URL_PMOC = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
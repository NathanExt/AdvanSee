from modulos.ad_users.active_directory_models.ad_user_database import ADUser, Base
from config import CONFIG
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class conecta_db:
    def __init__(self):
        self.session = None
        self.engine = create_engine(CONFIG.DATABASE_URL_USERS)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def search_name(self,term):
        if not self.session:
            return {'error': 'Conexão com banco PMOC não disponível'}

        return self.session.query(ADUser.email_address).filter(ADUser.sam_account_name == term).all()



con = conecta_db()
print(con.search_name('21a90208'))
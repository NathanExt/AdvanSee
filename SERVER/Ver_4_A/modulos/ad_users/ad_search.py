# -*- coding: utf-8 -*-
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modulos.ad_users.active_directory_models.ad_user_database import ADUser
from modulos.ad_users.ad_config import CONFIG_AD

class ACTIVE_DIRECTORY:
    def __init__(self):
        self.session = None
        self.engine = create_engine(CONFIG_AD.DATABASE_URL_USERS)
        session = sessionmaker(bind=self.engine)
        self.session = session()


    def search_user_by_id(self, user_id):
        print("USER_ID: ",user_id)

        # Buscar o usuário completo
        user = self.session.query(ADUser).filter(ADUser.sam_account_name == user_id).first()

        if user:
            user_data = {
                'display_name': user.display_name,
                'email_address': user.email_address,
                'given_name': user.given_name,
                'surname': user.surname,
                'enabled': user.enabled,
                'sam_account_name': user.sam_account_name
            }
        else:
            user_data = None

        print("USER_DATA: ",user_data)
        return user_data

    def search_user_by_email(self, email):
        # Buscar o usuário completo
        user = self.session.query(ADUser).filter(ADUser.sam_account_name == email).first()
        
        if user:
            user_data = {
                'display_name': user.display_name,
                'email_address': user.email_address,
                'given_name': user.given_name,
                'surname': user.surname,
                'enabled': user.enabled,
                'sam_account_name': user.sam_account_name
            }
        else:
            user_data = None
            
        return user_data


def search_ad_user(user_id):
    ad = ACTIVE_DIRECTORY()

    user_data = ad.search_user_by_id(user_id)
    if user_data: return user_data
    else: return None



if __name__ == "__main__":
    #a=ACTIVE_DIRECTORY()
    #print(a.search_user_by_id("2190208"))
    pass
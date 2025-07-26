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

        user_data = {
            'display_name' : self.session.query(ADUser.display_name).filter(ADUser.sam_account_name == user_id).all(),
            'email_address': self.session.query(ADUser.email_address).filter(ADUser.sam_account_name == user_id).all()
        }
        print("USER_DATA: ",user_data)
        return user_data

    def search_user_by_email(self, email):

        user_data = {
            'display_name' : self.session.query(ADUser.display_name).filter(ADUser.sam_account_name == email).all(),
            'email_address': self.session.query(ADUser.email_address).filter(ADUser.sam_account_name == email).all()
        }
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
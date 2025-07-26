from config import CONFIG
from modulos.ad_users.active_directory_models.ad_user_database import ADUser
from modulos.pmoc.pmoc_models.pmoc_database import Notebook, Desktop
from models.database import Asset,AssetSoftware


class MAIN:
    def __init__(self):
        self.db = ADUser()


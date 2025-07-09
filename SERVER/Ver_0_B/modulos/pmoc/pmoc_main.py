import json, os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modulos.pmoc.pmoc_models.pmoc_database import Base, Notebook
from modulos.pmoc.pmoc_config import CONFIG_PMOC
from modulos.pmoc.pmoc_notebook import notebook  # deve retornar um dicionário com os dados


class PMOC:
    def __init__(self):
        try:
            self.engine = create_engine(CONFIG_PMOC.DATABASE_URL)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
        except Exception as e:
            print("ERRO CONECTAR BANCO:", e)

    def criar_notebook(self, data):
        try:
            valor = float(data["equipmentValue"].replace("R$", "").replace(".", "").replace(",", "."))

            return Notebook(
                id=data["id"],
                model=data["model"],
                patrimony=data["patrimony"],
                manufacturer=data["manufacturer"],
                equipment_value=valor,
                tag_uisa=data["tagUisa"],
                created_at=datetime.strptime(data["createdAt"], "%Y-%m-%d").date(),
                updated_by=data["updated_by"],
                tag=data["tag"],
                os_version=data["osVersion"],
                entry_note=data["entryNote"],
                status=data["status"],
                date_home=datetime.strptime(data["dateHome"], "%Y-%m-%d").date(),
                date_end=datetime.strptime(data["dateEnd"], "%Y-%m-%d").date(),
                updated_at=datetime.strptime(data["updated_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
                rc=data["rc"],
                owner=data["owner"],
                processor=data["processor"],
                type=data["type"],
                ram_memory=data["ramMemory"],
                last_inventory_date=datetime.strptime(data["lastInventoryDate"], "%Y-%m-%d").date(),
                contract_type=data["contractType"],
                os_architecture=data["osArchitecture"]
            )
        except Exception as e:
            #print("Erro ao criar notebook:", e)
            return None

    def grava_dados(self):
        try:
            equipamentos = notebook()
            print(type(equipamentos))
            print(equipamentos)
            for equipamento_data in equipamentos:
                equip = self.criar_notebook(equipamento_data)
                if equip:
                    self.session.add(equip)

            self.session.commit()
            print("Todos os notebooks foram gravados com sucesso.")

        except Exception as e:
            self.session.rollback()
            print("Erro ao gravar notebooks:", e)

        finally:
            self.session.close()
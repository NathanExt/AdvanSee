import json, os
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from modulos.pmoc.pmoc_models.pmoc_database import Notebook, Desktop
from modulos.pmoc.pmoc_config import CONFIG_PMOC
from modulos.pmoc.pmoc_assets import notebook, desktop


class PMOC:
    def __init__(self):
        try:
            # Usar a URL do banco PMOC
            self.engine = create_engine(CONFIG_PMOC.DATABASE_URL_PMOC)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
        except Exception as e:
            print("ERRO CONECTAR BANCO:", e)


    def criar_notebook(self, data):
        try:
            equipment_value = data.get("equipmentValue", "R$0,00")
            if equipment_value and equipment_value != "":
                valor = float(equipment_value.replace("R$", "").replace(".", "").replace(",", "."))
            else:
                valor = 0.0
            
            created_at_str = data.get("createdAt", "")
            date_home_str = data.get("dateHome", "")
            date_end_str = data.get("dateEnd", "")
            last_inventory_date_str = data.get("lastInventoryDate", "")
            updated_at_str = data.get("updated_at", "")

            def parse_date(date_str, default_date=None):
                if date_str and date_str.strip():
                    try:
                        return datetime.strptime(date_str, "%Y-%m-%d").date()
                    except:
                        return default_date
                return default_date
            
            def parse_timestamp(timestamp_str, default_date=None):
                if timestamp_str and timestamp_str.strip():
                    try:
                        return datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                    except:
                        try:
                            return datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%f")
                        except:
                            return default_date
                return default_date
            
            print(data.get("id", "ID_NAO_ENCONTRADO"))
            
            notebook = Notebook()
            notebook.id = data.get("id", "")
            notebook.model = data.get("model", "")
            notebook.patrimony = data.get("patrimony", "")
            notebook.manufacturer = data.get("manufacturer", "")
            notebook.equipment_value = valor
            notebook.tag_uisa = data.get("tagUisa", "")
            notebook.created_at = parse_date(created_at_str)
            notebook.updated_by = data.get("updated_by", data.get("createdBy", ""))  # Usar createdBy como fallback
            notebook.tag = data.get("tag", "")
            notebook.os_version = data.get("osVersion", "")
            notebook.entry_note = data.get("entryNote", "")
            notebook.status = data.get("status", "")
            notebook.date_home = parse_date(date_home_str)
            notebook.date_end = parse_date(date_end_str)
            notebook.updated_at = parse_timestamp(updated_at_str)
            notebook.rc = data.get("rc", "")
            notebook.owner = data.get("owner", "")
            notebook.processor = data.get("processor", "")
            notebook.type = data.get("type", "")
            notebook.ram_memory = data.get("ramMemory", "")
            notebook.last_inventory_date = parse_date(last_inventory_date_str)
            notebook.contract_type = data.get("contractType", "")
            notebook.os_architecture = data.get("osArchitecture", "")
            return notebook
        except Exception as e:
            print(f"Erro ao criar notebook {data.get('id', 'ID_NAO_ENCONTRADO')}: {e}")
            return None

    def criar_desktop(self, data):
        try:
            equipment_value = data.get("equipmentValue", "R$0,00")
            if equipment_value and equipment_value != "":
                valor = float(equipment_value.replace("R$", "").replace(".", "").replace(",", "."))
            else:
                valor = 0.0
            
            created_at_str = data.get("createdAt", "")
            date_home_str = data.get("dateHome", "")
            date_end_str = data.get("dateEnd", "")
            last_inventory_date_str = data.get("lastInventoryDate", "")
            updated_at_str = data.get("updated_at", "")

            def parse_date(date_str, default_date=None):
                if date_str and date_str.strip():
                    try:
                        return datetime.strptime(date_str, "%Y-%m-%d").date()
                    except:
                        return default_date
                return default_date
            
            def parse_timestamp(timestamp_str, default_date=None):
                if timestamp_str and timestamp_str.strip():
                    try:
                        return datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                    except:
                        try:
                            return datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%f")
                        except:
                            return default_date
                return default_date
            
            desktop = Desktop()
            desktop.id = data.get("id", "")
            desktop.model = data.get("model", "")
            desktop.patrimony = data.get("patrimony", "")
            desktop.manufacturer = data.get("manufacturer", "")
            desktop.equipment_value = valor
            desktop.tag_uisa = data.get("tagUisa", "")
            desktop.created_at = parse_date(created_at_str)
            desktop.updated_by = data.get("updated_by", data.get("createdBy", ""))  # Usar createdBy como fallback
            desktop.tag = data.get("tag", "")
            desktop.os_version = data.get("osVersion", "")
            desktop.entry_note = data.get("entryNote", "")
            desktop.status = data.get("status", "")
            desktop.date_home = parse_date(date_home_str)
            desktop.date_end = parse_date(date_end_str)
            desktop.updated_at = parse_timestamp(updated_at_str)
            desktop.rc = data.get("rc", "")
            desktop.owner = data.get("owner", "")
            desktop.processor = data.get("processor", "")
            desktop.type = data.get("type", "")
            desktop.ram_memory = data.get("ramMemory", "")
            desktop.last_inventory_date = parse_date(last_inventory_date_str)
            desktop.contract_type = data.get("contractType", "")
            desktop.os_architecture = data.get("osArchitecture", "")
            return desktop
        except Exception as e:
            print(f"Erro ao criar Desktop {data.get('id', 'ID_NAO_ENCONTRADO')}: {e}")
            return None

    def grava_dados_notebook(self):
        try:
            equipamentos = notebook()
            print(f" Total de equipamentos encontrados: {len(equipamentos)}")
            
            sucessos = 0
            erros = 0
            
            for i, equipamento_data in enumerate(equipamentos, 1):
                equip = self.criar_notebook(equipamento_data)
                if equip:
                    try:
                        self.session.add(equip)
                        sucessos += 1
                        
                        # Commit a cada 50 registros para evitar timeout
                        if sucessos % 50 == 0:
                            self.session.commit()
                            print(f" {sucessos} registros processados...")
                    except Exception as e:
                        print(f" Erro ao adicionar registro {i}: {e}")
                        erros += 1
                else:
                    erros += 1

            # Commit final
            self.session.commit()
            print(f"\n Gravação concluída!")
            print(f"    Sucessos: {sucessos}")
            print(f"    Erros: {erros}")
            print(f"    Total: {len(equipamentos)}")

        except Exception as e:
            self.session.rollback()
            print(f" Erro ao gravar notebooks: {e}")

        finally:
            self.session.close()

    def grava_dados_desktop(self):
        try:
            equipamentos = desktop()
            print(f" Total de equipamentos encontrados: {len(equipamentos)}")
            
            sucessos = 0
            erros = 0
            
            for i, equipamento_data in enumerate(equipamentos, 1):
                equip = self.criar_desktop(equipamento_data)
                if equip:
                    try:
                        self.session.add(equip)
                        sucessos += 1
                        
                        # Commit a cada 50 registros para evitar timeout
                        if sucessos % 50 == 0:
                            self.session.commit()
                            print(f" {sucessos} registros processados...")
                    except Exception as e:
                        print(f" Erro ao adicionar registro {i}: {e}")
                        erros += 1
                else:
                    erros += 1

            # Commit final
            self.session.commit()
            print(f"\n Gravação concluída!")
            print(f"    Sucessos: {sucessos}")
            print(f"    Erros: {erros}")
            print(f"    Total: {len(equipamentos)}")

        except Exception as e:
            self.session.rollback()
            print(f" Erro ao gravar desktops: {e}")

        finally:
            self.session.close()

    def create_pmoc_tables(self):
        try:
            with self.engine.connect() as conn:
                # Verificar se a tabela notebook existe
                result = conn.execute(text("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = 'notebook'
                    );
                """))
                table_exists = result.scalar()
                if table_exists:
                    print("✅ Tabela 'notebook' já existe!")
                    return True
                else:
                    print("📋 Criando tabelas...")
                    # Criar tabelas usando SQL direto
                    conn.execute(text("""
                        CREATE TABLE notebook (
                            id VARCHAR(255) PRIMARY KEY,
                            model TEXT,
                            patrimony VARCHAR(255),
                            manufacturer TEXT,
                            equipment_value NUMERIC(10, 2),
                            tag_uisa VARCHAR(255),
                            created_at DATE,
                            updated_by VARCHAR(255),
                            tag VARCHAR(255),
                            os_version TEXT,
                            entry_note VARCHAR(255),
                            status VARCHAR(255),
                            date_home DATE,
                            date_end DATE,
                            updated_at TIMESTAMP,
                            rc VARCHAR(255),
                            owner VARCHAR(255),
                            processor TEXT,
                            type VARCHAR(255),
                            ram_memory VARCHAR(255),
                            last_inventory_date DATE,
                            contract_type VARCHAR(255),
                            os_architecture VARCHAR(255)
                        )
                    """))
                    
                    conn.execute(text("""
                        CREATE TABLE desktop (
                            id VARCHAR(255) PRIMARY KEY,
                            model TEXT,
                            patrimony VARCHAR(255),
                            manufacturer TEXT,
                            equipment_value NUMERIC(10, 2),
                            tag_uisa VARCHAR(255),
                            created_at DATE,
                            updated_by VARCHAR(255),
                            tag VARCHAR(255),
                            os_version TEXT,
                            entry_note VARCHAR(255),
                            status VARCHAR(255),
                            date_home DATE,
                            date_end DATE,
                            updated_at TIMESTAMP,
                            rc VARCHAR(255),
                            owner VARCHAR(255),
                            processor TEXT,
                            type VARCHAR(255),
                            ram_memory VARCHAR(255),
                            last_inventory_date DATE,
                            contract_type VARCHAR(255),
                            os_architecture VARCHAR(255)
                        )
                    """))
                    
                    conn.commit()
                    print("✅ Tabelas criadas com sucesso!")
                    return True
        except Exception as e:
            print(f" Erro ao criar tabelas: {e}")
            return False

    def main_pmoc(self):
        if self.create_pmoc_tables():
            self.grava_dados_notebook()
            self.grava_dados_desktop()
        else:
            print("Erro ao criar tabelas")







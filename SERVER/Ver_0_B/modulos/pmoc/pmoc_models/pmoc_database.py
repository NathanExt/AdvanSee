from sqlalchemy import Column, String, Date, Text, Numeric, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Notebook(Base):
    __tablename__ = 'notebook'

    id = Column(String, primary_key=True)
    model = Column(Text)
    patrimony = Column(String)
    manufacturer = Column(Text)
    equipment_value = Column(Numeric(10, 2))
    tag_uisa = Column(String)
    created_at = Column(Date)
    updated_by = Column(String)
    tag = Column(String)
    os_version = Column(Text)
    entry_note = Column(String)
    status = Column(String)
    date_home = Column(Date)
    date_end = Column(Date)
    updated_at = Column(TIMESTAMP)
    rc = Column(String)
    owner = Column(String)
    processor = Column(Text)
    type = Column(String)
    ram_memory = Column(String)
    last_inventory_date = Column(Date)
    contract_type = Column(String)
    os_architecture = Column(String)

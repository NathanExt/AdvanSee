from flask_sqlalchemy import SQLAlchemy


db_pmoc = SQLAlchemy()
class Notebook(db_pmoc.Model):
    __bind_key__ = 'pmoc'
    __tablename__ = 'notebook'

    id = db_pmoc.Column(db_pmoc.String(255), primary_key=True)
    model = db_pmoc.Column(db_pmoc.Text)
    patrimony = db_pmoc.Column(db_pmoc.String(255))
    manufacturer = db_pmoc.Column(db_pmoc.Text)
    equipment_value = db_pmoc.Column(db_pmoc.Numeric(10, 2))
    tag_uisa = db_pmoc.Column(db_pmoc.String(255))
    created_at = db_pmoc.Column(db_pmoc.Date)
    updated_by = db_pmoc.Column(db_pmoc.String(255))
    tag = db_pmoc.Column(db_pmoc.String(255))
    os_version = db_pmoc.Column(db_pmoc.Text)
    entry_note = db_pmoc.Column(db_pmoc.String(255))
    status = db_pmoc.Column(db_pmoc.String(255))
    date_home = db_pmoc.Column(db_pmoc.Date)
    date_end = db_pmoc.Column(db_pmoc.Date)
    updated_at = db_pmoc.Column(db_pmoc.DateTime)
    rc = db_pmoc.Column(db_pmoc.String(255))
    owner = db_pmoc.Column(db_pmoc.String(255))
    processor = db_pmoc.Column(db_pmoc.Text)
    type = db_pmoc.Column(db_pmoc.String(255))
    ram_memory = db_pmoc.Column(db_pmoc.String(255))
    last_inventory_date = db_pmoc.Column(db_pmoc.Date)
    contract_type = db_pmoc.Column(db_pmoc.String(255))
    os_architecture = db_pmoc.Column(db_pmoc.String(255))

    def __repr__(self):
        return f'<Notebook {self.id}>'

class Desktop(db_pmoc.Model):
    __bind_key__ = 'pmoc'
    __tablename__ = 'desktop'

    id = db_pmoc.Column(db_pmoc.String(255), primary_key=True)
    model = db_pmoc.Column(db_pmoc.Text)
    patrimony = db_pmoc.Column(db_pmoc.String(255))
    manufacturer = db_pmoc.Column(db_pmoc.Text)
    equipment_value = db_pmoc.Column(db_pmoc.Numeric(10, 2))
    tag_uisa = db_pmoc.Column(db_pmoc.String(255))
    created_at = db_pmoc.Column(db_pmoc.Date)
    updated_by = db_pmoc.Column(db_pmoc.String(255))
    tag = db_pmoc.Column(db_pmoc.String(255))
    os_version = db_pmoc.Column(db_pmoc.Text)
    entry_note = db_pmoc.Column(db_pmoc.String(255))
    status = db_pmoc.Column(db_pmoc.String(255))
    date_home = db_pmoc.Column(db_pmoc.Date)
    date_end = db_pmoc.Column(db_pmoc.Date)
    updated_at = db_pmoc.Column(db_pmoc.DateTime)
    rc = db_pmoc.Column(db_pmoc.String(255))
    owner = db_pmoc.Column(db_pmoc.String(255))
    processor = db_pmoc.Column(db_pmoc.Text)
    type = db_pmoc.Column(db_pmoc.String(255))
    ram_memory = db_pmoc.Column(db_pmoc.String(255))
    last_inventory_date = db_pmoc.Column(db_pmoc.Date)
    contract_type = db_pmoc.Column(db_pmoc.String(255))
    os_architecture = db_pmoc.Column(db_pmoc.String(255))

    def __repr__(self):
        return f'<Desktop {self.id}>'


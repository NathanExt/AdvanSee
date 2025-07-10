from models.database import db

class Notebook(db.Model):
    __bind_key__ = 'pmoc'
    __tablename__ = 'notebook'

    id = db.Column(db.String(255), primary_key=True)
    model = db.Column(db.Text)
    patrimony = db.Column(db.String(255))
    manufacturer = db.Column(db.Text)
    equipment_value = db.Column(db.Numeric(10, 2))
    tag_uisa = db.Column(db.String(255))
    created_at = db.Column(db.Date)
    updated_by = db.Column(db.String(255))
    tag = db.Column(db.String(255))
    os_version = db.Column(db.Text)
    entry_note = db.Column(db.String(255))
    status = db.Column(db.String(255))
    date_home = db.Column(db.Date)
    date_end = db.Column(db.Date)
    updated_at = db.Column(db.DateTime)
    rc = db.Column(db.String(255))
    owner = db.Column(db.String(255))
    processor = db.Column(db.Text)
    type = db.Column(db.String(255))
    ram_memory = db.Column(db.String(255))
    last_inventory_date = db.Column(db.Date)
    contract_type = db.Column(db.String(255))
    os_architecture = db.Column(db.String(255))

    def __repr__(self):
        return f'<Notebook {self.id}>'

class Desktop(db.Model):
    __bind_key__ = 'pmoc'
    __tablename__ = 'desktop'

    id = db.Column(db.String(255), primary_key=True)
    model = db.Column(db.Text)
    patrimony = db.Column(db.String(255))
    manufacturer = db.Column(db.Text)
    equipment_value = db.Column(db.Numeric(10, 2))
    tag_uisa = db.Column(db.String(255))
    created_at = db.Column(db.Date)
    updated_by = db.Column(db.String(255))
    tag = db.Column(db.String(255))
    os_version = db.Column(db.Text)
    entry_note = db.Column(db.String(255))
    status = db.Column(db.String(255))
    date_home = db.Column(db.Date)
    date_end = db.Column(db.Date)
    updated_at = db.Column(db.DateTime)
    rc = db.Column(db.String(255))
    owner = db.Column(db.String(255))
    processor = db.Column(db.Text)
    type = db.Column(db.String(255))
    ram_memory = db.Column(db.String(255))
    last_inventory_date = db.Column(db.Date)
    contract_type = db.Column(db.String(255))
    os_architecture = db.Column(db.String(255))

    def __repr__(self):
        return f'<Desktop {self.id}>'


#!/usr/bin/env python3
"""
Modelos SQLAlchemy para o banco de dados de usuários AD
"""
from datetime import datetime
from models.database import db

class ADUser(db.Model):
    """
    Modelo para a tabela ad_users
    Armazena informações de usuários do Active Directory
    """
    __bind_key__ = 'user'
    __tablename__ = 'ad_users'

    # Colunas da tabela
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(255))
    sam_account_name = db.Column(db.String(255), unique=True, nullable=False)
    given_name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    email_address = db.Column(db.String(255))
    enabled = db.Column(db.Boolean)
    last_logon_date = db.Column(db.DateTime)
    distinguished_name = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        """Representação string do objeto"""
        return f"{self.display_name},{self.sam_account_name},{self.email_address},{self.distinguished_name},{self.created_at},{self.updated_at}"



    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'display_name': self.display_name,
            'sam_account_name': self.sam_account_name,
            'given_name': self.given_name,
            'surname': self.surname,
            'email_address': self.email_address,
            'enabled': self.enabled,
            'last_logon_date': self.last_logon_date.isoformat() if self.last_logon_date else None,
            'distinguished_name': self.distinguished_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }






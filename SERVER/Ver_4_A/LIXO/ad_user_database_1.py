#!/usr/bin/env python3
"""
Modelos SQLAlchemy para o banco de dados de usuários AD
"""

from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

# Base para os modelos SQLAlchemy
Base = declarative_base()


class ADUser(Base):
    """
    Modelo para a tabela ad_users
    Armazena informações de usuários do Active Directory
    """
    __bind_key__ = 'user'
    __tablename__ = 'ad_users'

    # Colunas da tabela
    id = Column(Integer, primary_key=True)
    display_name = Column(String(255))
    sam_account_name = Column(String(255), unique=True, nullable=False)
    given_name = Column(String(255))
    surname = Column(String(255))
    email_address = Column(String(255))
    enabled = Column(Boolean)
    last_logon_date = Column(DateTime)
    distinguished_name = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
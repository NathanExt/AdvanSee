#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para testar os dois bancos de dados
"""

import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask
from config import CONFIG
from models.database import db, Organization, User, Asset
from modulos.pmoc.pmoc_models.pmoc_database import Notebook, Desktop

def test_dual_database():
    """Testa se os dois bancos de dados estão funcionando"""
    
    print("🧪 Testando configuração de dois bancos de dados...")
    
    # Criar aplicação Flask para teste
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG.DATABASE_URL_DEFAULT
    app.config['SQLALCHEMY_BINDS'] = CONFIG.SQLALCHEMY_BINDS
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = CONFIG.SQLALCHEMY_TRACK_MODIFICATIONS
    
    # Inicializar banco (única instância)
    db.init_app(app)
    
    with app.app_context():
        try:
            print("\n📊 Testando banco principal (ISAC)...")
            
            # Testar banco principal
            org_count = Organization.query.count()
            user_count = User.query.count()
            asset_count = Asset.query.count()
            
            print(f"✅ Banco principal funcionando!")
            print(f"   Organizações: {org_count}")
            print(f"   Usuários: {user_count}")
            print(f"   Assets: {asset_count}")
            
        except Exception as e:
            print(f"❌ Erro no banco principal: {e}")
            return False
        
        try:
            print("\n💻 Testando banco PMOC...")
            
            # Testar banco PMOC
            notebook_count = Notebook.query.count()
            desktop_count = Desktop.query.count()
            
            print(f"✅ Banco PMOC funcionando!")
            print(f"   Notebooks: {notebook_count}")
            print(f"   Desktops: {desktop_count}")
            
        except Exception as e:
            print(f"❌ Erro no banco PMOC: {e}")
            return False
    
    print("\n🎉 Ambos os bancos estão funcionando corretamente!")
    return True

def test_database_urls():
    """Testa se as URLs dos bancos estão corretas"""
    
    print("\n🔗 Verificando URLs dos bancos...")
    
    print(f"Banco Principal: {CONFIG.DATABASE_URL_DEFAULT}")
    print(f"Banco PMOC: {CONFIG.DATABASE_URL_PMOC}")
    
    # Verificar se as URLs são diferentes
    if CONFIG.DATABASE_URL_DEFAULT != CONFIG.DATABASE_URL_PMOC:
        print("✅ URLs dos bancos são diferentes (correto)")
    else:
        print("❌ URLs dos bancos são iguais (erro)")
        return False
    
    return True

def test_configuration():
    """Testa se a configuração está correta"""
    
    print("\n⚙️ Verificando configuração...")
    
    # Verificar se as configurações estão definidas
    required_configs = [
        'DATABASE_URL_DEFAULT',
        'DATABASE_URL_PMOC',
        'SQLALCHEMY_BINDS'
    ]
    
    for config in required_configs:
        if hasattr(CONFIG, config):
            print(f"✅ {config}: Configurado")
        else:
            print(f"❌ {config}: Não configurado")
            return False
    
    # Verificar SQLALCHEMY_BINDS
    if 'pmoc' in CONFIG.SQLALCHEMY_BINDS:
        print("✅ SQLALCHEMY_BINDS: Configurado corretamente")
    else:
        print("❌ SQLALCHEMY_BINDS: Não configurado corretamente")
        return False
    
    return True

def main():
    print("🚀 Iniciando testes de dois bancos de dados...")
    
    # Testar configuração
    if not test_configuration():
        print("❌ Falha na configuração")
        return
    
    # Testar URLs
    if not test_database_urls():
        print("❌ Falha nas URLs dos bancos")
        return
    
    # Testar bancos
    if not test_dual_database():
        print("❌ Falha nos bancos de dados")
        return
    
    print("\n🎉 Todos os testes passaram! Sistema configurado corretamente.")

if __name__ == "__main__":
    main() 
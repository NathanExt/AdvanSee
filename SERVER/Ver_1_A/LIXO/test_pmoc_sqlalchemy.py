#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de teste para o módulo PMOC com SQLAlchemy
"""

import sys
import os

# Adicionar o diretório raiz do projeto ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from modulos.pmoc.pmoc_main import PMOC

def main():
    print("🧪 Testando módulo PMOC com SQLAlchemy...")
    
    try:
        # Instanciar o módulo PMOC
        pmoc = PMOC()
        print("✅ Conexão com banco estabelecida!")
        
        # Testar criação de tabelas
        print("\n📋 Testando criação de tabelas...")
        if pmoc.create_pmoc_tables():
            print("✅ Tabelas criadas/verificadas com sucesso!")
        else:
            print("❌ Erro ao criar tabelas!")
            return
        
        # Testar gravação de notebooks
        print("\n💻 Testando gravação de notebooks...")
        pmoc.grava_dados_notebook()
        
        # Testar gravação de desktops
        print("\n🖥️ Testando gravação de desktops...")
        pmoc.grava_dados_desktop()
        
        print("\n🎉 Todos os testes concluídos com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 
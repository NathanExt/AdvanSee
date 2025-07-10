#!/usr/bin/env python3
"""
Script completo para gravar dados dos notebooks no banco DB_PMOC_1
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from modulos.pmoc.setup_pmoc_database import create_database, test_connection
from modulos.pmoc.create_pmoc_tables import create_pmoc_tables
from modulos.pmoc.pmoc_main import PMOC

def main():
    """Executa o processo completo de gravação dos notebooks"""
    
    print("🚀 Processo de Gravação de Notebooks - DB_PMOC_1")
    print("=" * 60)
    
    # Passo 1: Criar banco de dados
    print("\n📋 PASSO 1: Configurando banco de dados...")
    if not create_database():
        print("❌ Falha ao criar banco de dados.")
        return False
    
    # Passo 2: Testar conexão
    print("\n🔍 PASSO 2: Testando conexão...")
    if not test_connection():
        print("❌ Falha na conexão com o banco.")
        return False
    
    # Passo 3: Criar tabelas
    print("\n📋 PASSO 3: Criando tabelas...")
    if not create_pmoc_tables():
        print("❌ Falha ao criar tabelas.")
        return False
    
    # Passo 4: Gravar dados
    print("\n📊 PASSO 4: Gravando dados dos notebooks...")
    try:
        pmoc = PMOC()
        pmoc.grava_dados()
        print("\n✅ Processo concluído com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro durante a gravação: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Todos os dados foram gravados no banco DB_PMOC_1!")
    else:
        print("\n❌ Ocorreu um erro durante o processo.")
        sys.exit(1) 
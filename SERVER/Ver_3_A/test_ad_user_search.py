#!/usr/bin/env python3
"""
Script para testar a busca de usuários AD
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from modulos.ad_users.ad_search import search_ad_user

def test_ad_user_search():
    """Testa a busca de usuários AD"""
    
    print("🧪 Testando busca de usuários AD...")
    
    # Testar com um usuário específico
    test_user_id = "2190208"
    
    print(f"🔍 Buscando usuário: {test_user_id}")
    
    try:
        user_data = search_ad_user(test_user_id)
        
        if user_data:
            print("✅ Usuário encontrado!")
            print(f"📋 Dados do usuário:")
            print(f"   - Display Name: {user_data['display_name']}")
            print(f"   - Email: {user_data['email_address']}")
            print(f"   - Given Name: {user_data['given_name']}")
            print(f"   - Surname: {user_data['surname']}")
            print(f"   - Enabled: {user_data['enabled']}")
            print(f"   - SAM Account: {user_data['sam_account_name']}")
        else:
            print("❌ Usuário não encontrado")
            
    except Exception as e:
        print(f"❌ Erro ao buscar usuário: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ad_user_search() 
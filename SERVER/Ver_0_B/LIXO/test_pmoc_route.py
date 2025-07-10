#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para testar a rota PMOC
"""

import requests
import sys
import os

# URL base do servidor Flask
BASE_URL = "http://localhost:5000"

def test_pmoc_route():
    """Testa a rota principal do PMOC"""
    try:
        print("🧪 Testando rota PMOC...")
        
        # Testar rota principal
        response = requests.get(f"{BASE_URL}/pmoc")
        
        if response.status_code == 200:
            print("✅ Rota PMOC funcionando!")
            print(f"   Status Code: {response.status_code}")
            print(f"   Tamanho da resposta: {len(response.text)} bytes")
            
            # Verificar se contém elementos esperados
            if "Sistema PMOC" in response.text:
                print("✅ Template carregado corretamente")
            else:
                print("⚠️ Template pode não estar carregando corretamente")
                
            if "table" in response.text:
                print("✅ Tabela HTML presente")
            else:
                print("⚠️ Tabela HTML não encontrada")
                
        else:
            print(f"❌ Erro na rota PMOC: {response.status_code}")
            print(f"   Resposta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar ao servidor Flask")
        print("   Certifique-se de que o servidor está rodando em http://localhost:5000")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def test_pmoc_update():
    """Testa a rota de atualização do PMOC"""
    try:
        print("\n🔄 Testando rota de atualização PMOC...")
        
        response = requests.get(f"{BASE_URL}/pmoc_atualiza")
        
        if response.status_code == 200:
            print("✅ Rota de atualização funcionando!")
            print(f"   Status Code: {response.status_code}")
        else:
            print(f"❌ Erro na rota de atualização: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar ao servidor Flask")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def main():
    print("🚀 Iniciando testes da rota PMOC...")
    print(f"   URL Base: {BASE_URL}")
    
    test_pmoc_route()
    test_pmoc_update()
    
    print("\n🎉 Testes concluídos!")

if __name__ == "__main__":
    main() 
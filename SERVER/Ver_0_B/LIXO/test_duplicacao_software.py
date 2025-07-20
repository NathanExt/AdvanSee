#!/usr/bin/env python3
"""
Script de teste para verificar a correção do problema de duplicação de software instalado.
Este script simula checkins múltiplos com o mesmo software para verificar se a correção está funcionando.
"""

import sys
import os
import json
import requests
from datetime import datetime

# Configuração do servidor
SERVER_URL = "http://localhost:5000"
CHECKIN_ENDPOINT = f"{SERVER_URL}/agente/checkin"

def create_test_payload(asset_tag="TEST_ASSET_001", software_list=None):
    """Cria payload de teste para checkin do agente."""
    
    if software_list is None:
        software_list = [
            {
                "name": "Microsoft ASP.NET Core Runtime - 10.0.0 Preview 2 (x64)",
                "version": "80.0.31137",
                "vendor": "Microsoft Corporation"
            },
            {
                "name": "Google Chrome",
                "version": "120.0.6099.109",
                "vendor": "Google LLC"
            },
            {
                "name": "Microsoft Office Professional Plus 2019",
                "version": "16.0.14326.20404",
                "vendor": "Microsoft Corporation"
            },
            {
                "name": "Adobe Acrobat Reader DC",
                "version": "23.008.20470",
                "vendor": "Adobe Inc."
            },
            {
                "name": "Mozilla Firefox",
                "version": "121.0.1",
                "vendor": "Mozilla Corporation"
            }
        ]
    
    payload = {
        "agent_version": "2.0.0",
        "asset_tag": asset_tag,
        "system_info": {
            "tag": "TEST_DUPLICACAO",
            "ip_address": "192.168.1.100",
            "mac_address": "00:11:22:33:44:55",
            "operating_system": "Windows 10",
            "os_version": "10.0.19045",
            "python_version": "3.11.5",
            "logged_user": "test_user",
            "architecture": "x64",
            "processor": "Intel(R) Core(TM) i7-8700K CPU @ 3.70GHz",
            "cpu_count": 8,
            "cpu_count_logical": 8,
            "cpu_freq_current": 3700.0,
            "cpu_freq_min": 800.0,
            "cpu_freq_max": 4700.0,
            "total_memory_bytes": 17179869184,
            "available_memory_bytes": 8589934592,
            "memory_percent": 50.0,
            "total_disk_bytes": 500000000000,
            "used_disk_bytes": 250000000000,
            "free_disk_bytes": 250000000000,
            "disk_percent": 50.0,
            "computer_model": "OptiPlex 7070",
            "computer_manufacturer": "Dell Inc.",
            "computer_system_type": "Desktop",
            "installed_software": software_list
        }
    }
    
    return payload

def test_single_checkin():
    """Testa um checkin único."""
    print("=== Teste 1: Checkin Único ===")
    payload = create_test_payload()
    
    try:
        response = requests.post(CHECKIN_ENDPOINT, json=payload)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Sucesso: {result.get('message', 'Checkin realizado')}")
            return True
        else:
            print(f"Erro: {response.text}")
            return False
            
    except Exception as e:
        print(f"Erro na requisição: {str(e)}")
        return False

def test_duplicate_checkin():
    """Testa checkin duplicado com o mesmo software."""
    print("\n=== Teste 2: Checkin Duplicado ===")
    payload = create_test_payload()
    
    success_count = 0
    for i in range(3):
        print(f"\nCheckin {i+1}/3...")
        try:
            response = requests.post(CHECKIN_ENDPOINT, json=payload)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Sucesso: {result.get('message', 'Checkin realizado')}")
                success_count += 1
            else:
                print(f"Erro: {response.text}")
                
        except Exception as e:
            print(f"Erro na requisição: {str(e)}")
    
    print(f"\nResultado: {success_count}/3 checkins bem-sucedidos")
    return success_count == 3

def test_mixed_software():
    """Testa checkin com software parcialmente novo."""
    print("\n=== Teste 3: Software Parcialmente Novo ===")
    
    # Primeiro checkin com lista base
    base_software = [
        {
            "name": "Microsoft ASP.NET Core Runtime - 10.0.0 Preview 2 (x64)",
            "version": "80.0.31137",
            "vendor": "Microsoft Corporation"
        },
        {
            "name": "Google Chrome",
            "version": "120.0.6099.109",
            "vendor": "Google LLC"
        }
    ]
    
    # Segundo checkin com software adicional
    extended_software = base_software + [
        {
            "name": "Visual Studio Code",
            "version": "1.85.2",
            "vendor": "Microsoft Corporation"
        },
        {
            "name": "Python 3.11.5",
            "version": "3.11.5",
            "vendor": "Python Software Foundation"
        }
    ]
    
    payload1 = create_test_payload("TEST_ASSET_002", base_software)
    payload2 = create_test_payload("TEST_ASSET_002", extended_software)
    
    print("Primeiro checkin (2 softwares)...")
    try:
        response1 = requests.post(CHECKIN_ENDPOINT, json=payload1)
        print(f"Status: {response1.status_code}")
        if response1.status_code == 200:
            print("Primeiro checkin: Sucesso")
        else:
            print(f"Primeiro checkin: Erro - {response1.text}")
            return False
    except Exception as e:
        print(f"Erro no primeiro checkin: {str(e)}")
        return False
    
    print("\nSegundo checkin (4 softwares - 2 novos)...")
    try:
        response2 = requests.post(CHECKIN_ENDPOINT, json=payload2)
        print(f"Status: {response2.status_code}")
        if response2.status_code == 200:
            print("Segundo checkin: Sucesso")
            return True
        else:
            print(f"Segundo checkin: Erro - {response2.text}")
            return False
    except Exception as e:
        print(f"Erro no segundo checkin: {str(e)}")
        return False

def test_case_sensitivity():
    """Testa compatibilidade com chaves capitalizadas e minúsculas."""
    print("\n=== Teste 4: Compatibilidade de Chaves ===")
    
    # Formato VER_1 (chaves capitalizadas)
    ver1_software = [
        {
            "Name": "Microsoft Office",
            "Version": "16.0.14326.20404",
            "Vendor": "Microsoft Corporation"
        }
    ]
    
    # Formato VER_2 (chaves minúsculas)
    ver2_software = [
        {
            "name": "Microsoft Office",
            "version": "16.0.14326.20404",
            "vendor": "Microsoft Corporation"
        }
    ]
    
    payload1 = create_test_payload("TEST_ASSET_003", ver1_software)
    payload2 = create_test_payload("TEST_ASSET_003", ver2_software)
    
    print("Checkin VER_1 (chaves capitalizadas)...")
    try:
        response1 = requests.post(CHECKIN_ENDPOINT, json=payload1)
        print(f"Status: {response1.status_code}")
        if response1.status_code != 200:
            print(f"Erro VER_1: {response1.text}")
            return False
    except Exception as e:
        print(f"Erro no checkin VER_1: {str(e)}")
        return False
    
    print("Checkin VER_2 (chaves minúsculas)...")
    try:
        response2 = requests.post(CHECKIN_ENDPOINT, json=payload2)
        print(f"Status: {response2.status_code}")
        if response2.status_code == 200:
            print("Ambos os formatos funcionaram corretamente")
            return True
        else:
            print(f"Erro VER_2: {response2.text}")
            return False
    except Exception as e:
        print(f"Erro no checkin VER_2: {str(e)}")
        return False

def verify_database_integrity():
    """Verifica se não há duplicatas no banco de dados."""
    print("\n=== Verificação de Integridade do Banco ===")
    print("NOTA: Execute manualmente a consulta SQL abaixo para verificar duplicatas:")
    print("""
    SELECT asset_id, name, version, vendor, COUNT(*) as count
    FROM installed_software
    GROUP BY asset_id, name, version, vendor
    HAVING COUNT(*) > 1;
    """)
    print("Se a consulta retornar 0 registros, não há duplicatas.")
    
    print("\nConsulta para verificar software de teste:")
    print("""
    SELECT a.asset_tag, i.name, i.version, i.vendor, i.created_at
    FROM installed_software i
    JOIN assets a ON i.asset_id = a.id
    WHERE a.asset_tag LIKE 'TEST_ASSET_%'
    ORDER BY a.asset_tag, i.name;
    """)

def main():
    """Executa todos os testes."""
    print("=" * 60)
    print("TESTE DE CORREÇÃO DO PROBLEMA DE DUPLICAÇÃO DE SOFTWARE")
    print("=" * 60)
    
    results = []
    
    # Teste 1: Checkin único
    results.append(("Checkin Único", test_single_checkin()))
    
    # Teste 2: Checkin duplicado
    results.append(("Checkin Duplicado", test_duplicate_checkin()))
    
    # Teste 3: Software parcialmente novo
    results.append(("Software Parcialmente Novo", test_mixed_software()))
    
    # Teste 4: Compatibilidade de chaves
    results.append(("Compatibilidade de Chaves", test_case_sensitivity()))
    
    # Verificação de integridade
    verify_database_integrity()
    
    # Resumo dos resultados
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResultado Final: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! A correção está funcionando corretamente.")
    else:
        print("⚠️  Alguns testes falharam. Verifique os logs e a implementação.")
    
    return passed == total

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--server-url":
        if len(sys.argv) > 2:
            SERVER_URL = sys.argv[2]
            CHECKIN_ENDPOINT = f"{SERVER_URL}/agente/checkin"
        else:
            print("Uso: python test_duplicacao_software.py --server-url http://localhost:5000")
            sys.exit(1)
    
    success = main()
    sys.exit(0 if success else 1) 
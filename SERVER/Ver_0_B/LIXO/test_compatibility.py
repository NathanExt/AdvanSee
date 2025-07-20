#!/usr/bin/env python3
"""
Script de teste para validar a compatibilidade entre agente VER_1 e VER_2
Simula dados de checkin com diferentes formatos de chaves
"""

import json
import requests
from cryptography.fernet import Fernet

# Configurações (ajustar conforme necessário)
SERVER_URL = "http://127.0.0.1:5000/checkin"
ENCRYPTION_KEY = b'Xexalh4dXCIzMeilnbXok34y5Jx_J5DRP9lR98Yx0rc='
CIPHER_SUITE = Fernet(ENCRYPTION_KEY)

def create_test_data_ver1():
    """Simula dados do agente VER_1 (chaves capitalizadas)"""
    return {
        'asset_tag': 'TEST-VER1-001',
        'agent_version': '1.0.0',
        'system_info': {
            'system_uuid': 'test-uuid-ver1-001',
            'tag': 'BIOS-SN-VER1-001',
            'hostname': 'TEST-PC-VER1',
            'ip_address': '192.168.1.100',
            'mac_address': '00:11:22:33:44:55',
            'operating_system': 'Windows 10 Pro',
            'installed_software': [
                {
                    "Name": "Microsoft Office",
                    "Version": "16.0.123",
                    "Vendor": "Microsoft Corporation"
                },
                {
                    "Name": "Google Chrome",
                    "Version": "120.0.1",
                    "Vendor": "Google LLC"
                },
                {
                    "Name": "Adobe Reader",
                    "Version": "2023.1",
                    "Vendor": "Adobe Inc."
                }
            ]
        },
        'timestamp': '2024-01-15T10:30:00.000Z'
    }

def create_test_data_ver2():
    """Simula dados do agente VER_2 (chaves minúsculas)"""
    return {
        'asset_tag': 'TEST-VER2-002',
        'agent_version': '2.0.0',
        'system_info': {
            'system_uuid': 'test-uuid-ver2-002',
            'tag': 'BIOS-SN-VER2-002',
            'hostname': 'TEST-PC-VER2',
            'ip_address': '192.168.1.101',
            'mac_address': '00:11:22:33:44:66',
            'operating_system': 'Windows 11 Pro',
            'installed_software': [
                {
                    "name": "Microsoft Office",
                    "version": "16.0.125",
                    "vendor": "Microsoft Corporation"
                },
                {
                    "name": "Mozilla Firefox",
                    "version": "121.0",
                    "vendor": "Mozilla Corporation"
                },
                {
                    "name": "VLC Media Player",
                    "version": "3.0.18",
                    "vendor": "VideoLAN"
                }
            ]
        },
        'timestamp': '2024-01-15T10:35:00.000Z'
    }

def create_test_data_mixed():
    """Simula dados mistos (alguns com chaves capitalizadas, outros minúsculas)"""
    return {
        'asset_tag': 'TEST-MIXED-003',
        'agent_version': '1.5.0',
        'system_info': {
            'system_uuid': 'test-uuid-mixed-003',
            'tag': 'BIOS-SN-MIXED-003',
            'hostname': 'TEST-PC-MIXED',
            'ip_address': '192.168.1.102',
            'mac_address': '00:11:22:33:44:77',
            'operating_system': 'Windows 10 Enterprise',
            'installed_software': [
                {
                    "Name": "Microsoft Office",  # Capitalizada
                    "Version": "16.0.124",
                    "Vendor": "Microsoft Corporation"
                },
                {
                    "name": "Visual Studio Code",  # Minúscula
                    "version": "1.85.0",
                    "vendor": "Microsoft Corporation"
                },
                {
                    "Name": "Notepad++",  # Capitalizada
                    "version": "8.5.8",   # Minúscula (campo misto)
                    "Vendor": "Don Ho"
                }
            ]
        },
        'timestamp': '2024-01-15T10:40:00.000Z'
    }

def send_checkin_data(test_data, test_name):
    """Envia dados de checkin para o servidor"""
    try:
        print(f"\n{'='*50}")
        print(f"TESTE: {test_name}")
        print(f"{'='*50}")
        
        # Preparar dados criptografados
        json_data = json.dumps(test_data).encode('utf-8')
        encrypted_data = CIPHER_SUITE.encrypt(json_data)
        
        payload = {
            "encrypted_payload": encrypted_data.decode('latin-1')
        }
        
        # Enviar para o servidor
        print(f"Enviando checkin para: {test_data['asset_tag']}")
        print(f"Software instalado: {len(test_data['system_info']['installed_software'])} itens")
        
        response = requests.post(SERVER_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            print("✅ SUCESSO: Checkin processado com sucesso")
            try:
                response_data = response.json()
                print(f"Resposta: {response_data}")
            except:
                print("Resposta recebida (não JSON)")
        else:
            print(f"❌ ERRO: Status {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ EXCEÇÃO: {e}")

def main():
    """Executa todos os testes de compatibilidade"""
    print("🚀 INICIANDO TESTES DE COMPATIBILIDADE")
    print("Testando a compatibilidade entre agente VER_1 e VER_2 com servidor Ver_0_B")
    
    # Teste 1: Agente VER_1 (chaves capitalizadas)
    test_data_ver1 = create_test_data_ver1()
    send_checkin_data(test_data_ver1, "AGENTE VER_1 (Chaves Capitalizadas)")
    
    # Teste 2: Agente VER_2 (chaves minúsculas)
    test_data_ver2 = create_test_data_ver2()
    send_checkin_data(test_data_ver2, "AGENTE VER_2 (Chaves Minúsculas)")
    
    # Teste 3: Dados mistos (compatibilidade total)
    test_data_mixed = create_test_data_mixed()
    send_checkin_data(test_data_mixed, "DADOS MISTOS (Teste de Robustez)")
    
    print(f"\n{'='*50}")
    print("🏁 TESTES CONCLUÍDOS")
    print("{'='*50}")
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Verificar logs do servidor para confirmar processamento")
    print("2. Consultar banco de dados para validar software instalado")
    print("3. Acessar página /software para verificar dados na interface")
    print("\n💡 DICA: Use a página de software para visualizar os resultados dos testes")

if __name__ == "__main__":
    main() 
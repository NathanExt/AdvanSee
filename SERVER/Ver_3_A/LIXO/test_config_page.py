#!/usr/bin/env python3
"""
Script para testar a página de configurações
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes.rotas_site.rt_config import get_user_config, save_user_config, DEFAULT_CONFIG, TIMEZONES, LANGUAGES, THEMES
from datetime import datetime
import pytz

def test_config_functions():
    """Testa as funções de configuração"""
    
    print("=== TESTE DAS FUNÇÕES DE CONFIGURAÇÃO ===")
    
    # Teste 1: Configuração padrão
    print("\n1. Testando configuração padrão:")
    default_config = get_user_config()
    print(f"   Configuração padrão: {default_config}")
    
    # Teste 2: Salvar configuração personalizada
    print("\n2. Testando salvamento de configuração:")
    custom_config = {
        'timezone': 'America/New_York',
        'language': 'en-US',
        'theme': 'dark',
        'date_format': 'MM/DD/YYYY',
        'time_format': '12h'
    }
    
    try:
        save_user_config(custom_config)
        print(f"   ✅ Configuração personalizada salva: {custom_config}")
    except Exception as e:
        print(f"   ❌ Erro ao salvar: {e}")
    
    # Teste 3: Verificar configuração salva
    print("\n3. Verificando configuração salva:")
    saved_config = get_user_config()
    print(f"   Configuração atual: {saved_config}")
    
    # Teste 4: Testar fusos horários
    print("\n4. Testando fusos horários:")
    for tz_info in TIMEZONES[:3]:  # Apenas os primeiros 3
        try:
            tz = pytz.timezone(tz_info['value'])
            current_time = datetime.now(tz).strftime('%H:%M:%S')
            print(f"   {tz_info['label']}: {current_time}")
        except Exception as e:
            print(f"   ❌ Erro com {tz_info['value']}: {e}")
    
    # Teste 5: Verificar idiomas disponíveis
    print("\n5. Idiomas disponíveis:")
    for lang in LANGUAGES:
        print(f"   {lang['flag']} {lang['label']} ({lang['value']})")
    
    # Teste 6: Verificar temas disponíveis
    print("\n6. Temas disponíveis:")
    for theme in THEMES:
        print(f"   {theme['label']}: {theme['description']}")

def test_timezone_conversions():
    """Testa conversões de fuso horário"""
    
    print("\n=== TESTE DE CONVERSÕES DE FUSO HORÁRIO ===")
    
    # Hora atual em UTC
    utc_now = datetime.utcnow()
    print(f"Hora UTC: {utc_now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Converter para diferentes fusos
    test_timezones = [
        'America/Sao_Paulo',
        'America/New_York',
        'Europe/London',
        'Asia/Tokyo'
    ]
    
    for tz_name in test_timezones:
        try:
            tz = pytz.timezone(tz_name)
            local_time = utc_now.replace(tzinfo=pytz.UTC).astimezone(tz)
            print(f"{tz_name}: {local_time.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"❌ Erro com {tz_name}: {e}")

def test_config_validation():
    """Testa validação de configurações"""
    
    print("\n=== TESTE DE VALIDAÇÃO DE CONFIGURAÇÕES ===")
    
    # Teste 1: Configuração válida
    valid_config = {
        'timezone': 'America/Sao_Paulo',
        'language': 'pt-BR',
        'theme': 'light',
        'date_format': 'DD/MM/YYYY',
        'time_format': '24h'
    }
    
    print("1. Configuração válida:")
    print(f"   {valid_config}")
    
    # Teste 2: Configuração inválida
    invalid_config = {
        'timezone': 'Invalid/Timezone',
        'language': 'invalid-lang',
        'theme': 'invalid-theme',
        'date_format': 'INVALID',
        'time_format': 'invalid'
    }
    
    print("\n2. Configuração inválida:")
    print(f"   {invalid_config}")
    
    # Teste 3: Verificar se timezone é válido
    print("\n3. Validação de timezone:")
    for tz_name in ['America/Sao_Paulo', 'Invalid/Timezone']:
        try:
            pytz.timezone(tz_name)
            print(f"   ✅ {tz_name}: Válido")
        except pytz.exceptions.UnknownTimeZoneError:
            print(f"   ❌ {tz_name}: Inválido")

def test_config_persistence():
    """Testa persistência de configurações"""
    
    print("\n=== TESTE DE PERSISTÊNCIA DE CONFIGURAÇÕES ===")
    
    # Simular configurações de diferentes usuários
    test_configs = [
        {
            'user': 'user1',
            'config': {
                'timezone': 'America/Sao_Paulo',
                'language': 'pt-BR',
                'theme': 'light'
            }
        },
        {
            'user': 'user2',
            'config': {
                'timezone': 'America/New_York',
                'language': 'en-US',
                'theme': 'dark'
            }
        },
        {
            'user': 'user3',
            'config': {
                'timezone': 'Europe/London',
                'language': 'en-US',
                'theme': 'auto'
            }
        }
    ]
    
    for test_case in test_configs:
        print(f"\nUsuário: {test_case['user']}")
        print(f"Configuração: {test_case['config']}")
        
        # Simular salvamento
        try:
            save_user_config(test_case['config'])
            saved = get_user_config()
            print(f"✅ Salvo e recuperado: {saved}")
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    try:
        print("🧪 TESTE DA PÁGINA DE CONFIGURAÇÕES")
        print("=" * 50)
        
        test_config_functions()
        test_timezone_conversions()
        test_config_validation()
        test_config_persistence()
        
        print("\n" + "=" * 50)
        print("✅ Todos os testes concluídos!")
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc() 
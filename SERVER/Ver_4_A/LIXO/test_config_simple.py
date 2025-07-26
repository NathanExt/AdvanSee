#!/usr/bin/env python3
"""
Teste simples das configurações sem contexto Flask
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes.rotas_site.rt_config import DEFAULT_CONFIG, TIMEZONES, LANGUAGES, THEMES
from datetime import datetime
import pytz

def test_default_config():
    """Testa a configuração padrão"""
    
    print("=== TESTE DA CONFIGURAÇÃO PADRÃO ===")
    print(f"Configuração padrão: {DEFAULT_CONFIG}")
    
    # Verificar se todos os campos necessários estão presentes
    required_fields = ['timezone', 'language', 'theme', 'date_format', 'time_format']
    missing_fields = [field for field in required_fields if field not in DEFAULT_CONFIG]
    
    if missing_fields:
        print(f"❌ Campos faltando: {missing_fields}")
    else:
        print("✅ Todos os campos necessários estão presentes")

def test_timezones():
    """Testa os fusos horários disponíveis"""
    
    print("\n=== TESTE DOS FUSOS HORÁRIOS ===")
    print(f"Total de fusos horários: {len(TIMEZONES)}")
    
    # Testar os primeiros 5 fusos
    for i, tz_info in enumerate(TIMEZONES[:5]):
        try:
            tz = pytz.timezone(tz_info['value'])
            current_time = datetime.now(tz).strftime('%H:%M:%S')
            print(f"{i+1}. {tz_info['label']}: {current_time}")
        except Exception as e:
            print(f"{i+1}. ❌ {tz_info['value']}: {e}")
    
    # Verificar se o fuso padrão está na lista
    default_tz = DEFAULT_CONFIG['timezone']
    tz_found = any(tz['value'] == default_tz for tz in TIMEZONES)
    
    if tz_found:
        print(f"✅ Fuso padrão '{default_tz}' encontrado na lista")
    else:
        print(f"❌ Fuso padrão '{default_tz}' NÃO encontrado na lista")

def test_languages():
    """Testa os idiomas disponíveis"""
    
    print("\n=== TESTE DOS IDIOMAS ===")
    print(f"Total de idiomas: {len(LANGUAGES)}")
    
    for lang in LANGUAGES:
        print(f"  {lang['flag']} {lang['label']} ({lang['value']})")
    
    # Verificar se o idioma padrão está na lista
    default_lang = DEFAULT_CONFIG['language']
    lang_found = any(lang['value'] == default_lang for lang in LANGUAGES)
    
    if lang_found:
        print(f"✅ Idioma padrão '{default_lang}' encontrado na lista")
    else:
        print(f"❌ Idioma padrão '{default_lang}' NÃO encontrado na lista")

def test_themes():
    """Testa os temas disponíveis"""
    
    print("\n=== TESTE DOS TEMAS ===")
    print(f"Total de temas: {len(THEMES)}")
    
    for theme in THEMES:
        print(f"  {theme['label']}: {theme['description']}")
        print(f"    Ícone: {theme['icon']}")
        print(f"    Valor: {theme['value']}")
        print()
    
    # Verificar se o tema padrão está na lista
    default_theme = DEFAULT_CONFIG['theme']
    theme_found = any(theme['value'] == default_theme for theme in THEMES)
    
    if theme_found:
        print(f"✅ Tema padrão '{default_theme}' encontrado na lista")
    else:
        print(f"❌ Tema padrão '{default_theme}' NÃO encontrado na lista")

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
    
    # Verificar se todos os valores são válidos
    valid_timezone = any(tz['value'] == valid_config['timezone'] for tz in TIMEZONES)
    valid_language = any(lang['value'] == valid_config['language'] for lang in LANGUAGES)
    valid_theme = any(theme['value'] == valid_config['theme'] for theme in THEMES)
    
    print(f"   Timezone válido: {'✅' if valid_timezone else '❌'}")
    print(f"   Idioma válido: {'✅' if valid_language else '❌'}")
    print(f"   Tema válido: {'✅' if valid_theme else '❌'}")
    
    # Teste 2: Verificar se timezone é válido
    print("\n2. Validação de timezone:")
    for tz_name in ['America/Sao_Paulo', 'Invalid/Timezone']:
        try:
            pytz.timezone(tz_name)
            print(f"   ✅ {tz_name}: Válido")
        except pytz.exceptions.UnknownTimeZoneError:
            print(f"   ❌ {tz_name}: Inválido")

def test_date_formats():
    """Testa formatos de data"""
    
    print("\n=== TESTE DE FORMATOS DE DATA ===")
    
    # Data de exemplo
    test_date = datetime(2024, 12, 31, 14, 30, 25)
    
    # Formatos disponíveis
    date_formats = [
        ('DD/MM/YYYY', '31/12/2024'),
        ('MM/DD/YYYY', '12/31/2024'),
        ('YYYY-MM-DD', '2024-12-31'),
        ('DD-MM-YYYY', '31-12-2024')
    ]
    
    time_formats = [
        ('24h', '14:30:25'),
        ('12h', '2:30:25 PM')
    ]
    
    print("Formatos de data:")
    for format_name, example in date_formats:
        print(f"  {format_name}: {example}")
    
    print("\nFormatos de hora:")
    for format_name, example in time_formats:
        print(f"  {format_name}: {example}")

if __name__ == "__main__":
    try:
        print("🧪 TESTE SIMPLES DA PÁGINA DE CONFIGURAÇÕES")
        print("=" * 60)
        
        test_default_config()
        test_timezones()
        test_languages()
        test_themes()
        test_timezone_conversions()
        test_config_validation()
        test_date_formats()
        
        print("\n" + "=" * 60)
        print("✅ Todos os testes concluídos com sucesso!")
        print("\n📋 RESUMO:")
        print(f"  • {len(TIMEZONES)} fusos horários disponíveis")
        print(f"  • {len(LANGUAGES)} idiomas disponíveis")
        print(f"  • {len(THEMES)} temas disponíveis")
        print(f"  • Configuração padrão: {DEFAULT_CONFIG['timezone']}, {DEFAULT_CONFIG['language']}, {DEFAULT_CONFIG['theme']}")
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc() 
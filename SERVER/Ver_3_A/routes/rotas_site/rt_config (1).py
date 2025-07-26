from flask import Blueprint, render_template, flash, redirect, request, url_for, session, jsonify
from models.database import db, Asset, AssetSoftware, AssetVulnerability, AssetPatch, Agent, AssetHistory, InstalledSoftware, NetworkInterface, WindowsUpdate, PmocAsset
from comand.comands import COMANDOS
from modulos.pmoc.pmoc_search import search_pmoc_asset
import os
import json
from datetime import datetime
import pytz

bp_config = Blueprint('config', __name__)

# Configurações padrão
DEFAULT_CONFIG = {
    'timezone': 'America/Sao_Paulo',
    'language': 'pt-BR',
    'theme': 'light',
    'date_format': 'DD/MM/YYYY',
    'time_format': '24h'
}

# Fusos horários disponíveis
TIMEZONES = [
    {'value': 'America/Sao_Paulo', 'label': 'Brasília (UTC-3)'},
    {'value': 'America/Cuiaba', 'label': 'Cuiabá-MT (UTC-4)'},
    {'value': 'America/Manaus', 'label': 'Manaus (UTC-4)'},
    {'value': 'America/Belem', 'label': 'Belém (UTC-3)'},
    {'value': 'America/Fortaleza', 'label': 'Fortaleza (UTC-3)'},
    {'value': 'America/Recife', 'label': 'Recife (UTC-3)'},
    {'value': 'America/Maceio', 'label': 'Maceió (UTC-3)'},
    {'value': 'America/Aracaju', 'label': 'Aracaju (UTC-3)'},
    {'value': 'America/Salvador', 'label': 'Salvador (UTC-3)'},
    {'value': 'America/Bahia', 'label': 'Bahia (UTC-3)'},
    {'value': 'America/Noronha', 'label': 'Fernando de Noronha (UTC-2)'},
    {'value': 'UTC', 'label': 'UTC (UTC+0)'},
    {'value': 'America/New_York', 'label': 'Nova York (UTC-5)'},
    {'value': 'Europe/London', 'label': 'Londres (UTC+0)'},
    {'value': 'Europe/Paris', 'label': 'Paris (UTC+1)'},
    {'value': 'Asia/Tokyo', 'label': 'Tóquio (UTC+9)'},
]

# Idiomas disponíveis
LANGUAGES = [
    {'value': 'pt-BR', 'label': 'Português (Brasil)', 'flag': '🇧🇷'},
    {'value': 'en-US', 'label': 'English (US)', 'flag': '🇺🇸'},
    {'value': 'es-ES', 'label': 'Español', 'flag': '🇪🇸'},
    {'value': 'fr-FR', 'label': 'Français', 'flag': '🇫🇷'},
    {'value': 'de-DE', 'label': 'Deutsch', 'flag': '🇩🇪'},
    {'value': 'it-IT', 'label': 'Italiano', 'flag': '🇮🇹'},
    {'value': 'ja-JP', 'label': '日本語', 'flag': '🇯🇵'},
    {'value': 'zh-CN', 'label': '中文', 'flag': '🇨🇳'},
]

# Temas disponíveis
THEMES = [
    {'value': 'light', 'label': 'Claro', 'icon': 'bi-sun', 'description': 'Tema claro padrão'},
    {'value': 'dark', 'label': 'Escuro', 'icon': 'bi-moon', 'description': 'Tema escuro'},
    {'value': 'auto', 'label': 'Automático', 'icon': 'bi-circle-half', 'description': 'Segue a preferência do sistema'},
    {'value': 'blue', 'label': 'Azul', 'icon': 'bi-palette', 'description': 'Tema azul corporativo'},
    {'value': 'green', 'label': 'Verde', 'icon': 'bi-palette', 'description': 'Tema verde natureza'},
]

def get_user_config():
    """Obtém as configurações do usuário da sessão"""
    user_config = session.get('user_config', {})
    # Mesclar com configurações padrão
    config = DEFAULT_CONFIG.copy()
    config.update(user_config)
    return config

def save_user_config(config):
    """Salva as configurações do usuário na sessão"""
    session['user_config'] = config
    session.modified = True

@bp_config.route('/config')
def config():
    """Página principal de configurações"""
    user_config = get_user_config()
    
    # Obter hora atual em diferentes fusos para demonstração
    current_times = {}
    for tz_info in TIMEZONES[:5]:  # Apenas os primeiros 5 para demonstração
        try:
            tz = pytz.timezone(tz_info['value'])
            current_times[tz_info['value']] = datetime.now(tz).strftime('%H:%M:%S')
        except:
            current_times[tz_info['value']] = '--:--:--'
    
    return render_template('config.html',
                         user_config=user_config,
                         timezones=TIMEZONES,
                         languages=LANGUAGES,
                         themes=THEMES,
                         current_times=current_times)

@bp_config.route('/config/save', methods=['POST'])
def save_config():
    """Salva as configurações do usuário"""
    try:
        data = request.get_json()
        
        # Validar dados recebidos
        if not data:
            return jsonify({'success': False, 'message': 'Dados inválidos'}), 400
        
        # Obter configurações atuais
        current_config = get_user_config()
        
        # Atualizar configurações
        if 'timezone' in data:
            current_config['timezone'] = data['timezone']
        if 'language' in data:
            current_config['language'] = data['language']
        if 'theme' in data:
            current_config['theme'] = data['theme']
        if 'date_format' in data:
            current_config['date_format'] = data['date_format']
        if 'time_format' in data:
            current_config['time_format'] = data['time_format']
        
        # Salvar configurações
        save_user_config(current_config)
        
        return jsonify({
            'success': True, 
            'message': 'Configurações salvas com sucesso!',
            'config': current_config
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro ao salvar configurações: {str(e)}'}), 500

@bp_config.route('/config/reset', methods=['POST'])
def reset_config():
    """Reseta as configurações para os valores padrão"""
    try:
        # Remover configurações da sessão
        session.pop('user_config', None)
        
        return jsonify({
            'success': True, 
            'message': 'Configurações resetadas para os valores padrão!',
            'config': DEFAULT_CONFIG
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro ao resetar configurações: {str(e)}'}), 500

@bp_config.route('/config/preview/<setting_type>/<value>')
def preview_config(setting_type, value):
    """Preview das configurações"""
    try:
        if setting_type == 'timezone':
            tz = pytz.timezone(value)
            current_time = datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')
            return jsonify({
                'success': True,
                'preview': f'Hora atual: {current_time}',
                'timezone': value
            })
        elif setting_type == 'theme':
            return jsonify({
                'success': True,
                'preview': f'Visualizará o tema {value}',
                'theme': value
            })
        else:
            return jsonify({
                'success': True,
                'preview': f'Configuração: {value}',
                'setting': value
            })
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro ao gerar preview: {str(e)}'}), 500

@bp_config.route('/config/get-config')
def get_config():
    """Obtém as configurações do usuário"""
    try:
        user_config = get_user_config()
        return jsonify({
            'success': True,
            'config': user_config
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro ao obter configurações: {str(e)}'}), 500

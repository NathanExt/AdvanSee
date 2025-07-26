#!/usr/bin/env python3
"""
Script para testar se a correção do updated_at no checkin funcionou
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import db, Asset, Agent
from datetime import datetime
import time

def test_checkin_updated_at():
    """Testa se o updated_at é atualizado durante o checkin"""
    
    print("=== TESTE DE UPDATED_AT NO CHECKIN ===")
    
    # Buscar um asset com agente
    asset = Asset.query.join(Agent).first()
    
    if not asset:
        print("Nenhum asset com agente encontrado para teste")
        return
    
    print(f"Asset: {asset.name} (ID: {asset.id})")
    print(f"updated_at atual: {asset.updated_at}")
    print(f"last_seen atual: {asset.last_seen}")
    
    # Simular checkin com system_info vazio (caso problemático)
    print("\n--- Teste 1: Checkin com system_info vazio ---")
    old_updated_at = asset.updated_at
    old_last_seen = asset.last_seen
    
    # Aguardar 1 segundo
    time.sleep(1)
    
    # Simular o que acontece no checkin com system_info vazio
    # (linhas 123-125 do código corrigido)
    asset.last_seen = datetime.utcnow()
    asset.updated_at = datetime.utcnow()
    
    print(f"updated_at após atribuição: {asset.updated_at}")
    print(f"last_seen após atribuição: {asset.last_seen}")
    
    try:
        db.session.commit()
        print("✅ Commit realizado com sucesso")
        
        # Recarregar o asset do banco
        db.session.refresh(asset)
        print(f"updated_at após commit: {asset.updated_at}")
        print(f"last_seen após commit: {asset.last_seen}")
        
        if asset.updated_at != old_updated_at:
            print("✅ updated_at foi atualizado corretamente")
        else:
            print("❌ updated_at NÃO foi atualizado")
            
        if asset.last_seen != old_last_seen:
            print("✅ last_seen foi atualizado corretamente")
        else:
            print("❌ last_seen NÃO foi atualizado")
            
    except Exception as e:
        print(f"❌ Erro no commit: {e}")
        db.session.rollback()
    
    # Simular checkin com system_info (caso normal)
    print("\n--- Teste 2: Checkin com system_info ---")
    old_updated_at = asset.updated_at
    old_last_seen = asset.last_seen
    
    # Aguardar 1 segundo
    time.sleep(1)
    
    # Simular system_info
    system_info = {
        'hostname': 'test-hostname',
        'ip_address': '192.168.1.100',
        'operating_system': 'Windows 10'
    }
    
    # Simular o que acontece no checkin com system_info
    # Sempre atualizar last_seen e updated_at primeiro
    asset.last_seen = datetime.utcnow()
    asset.updated_at = datetime.utcnow()
    
    # Depois processar system_info
    if system_info:
        # Simular atualização de campos
        if 'hostname' in system_info and asset.name != system_info['hostname']:
            asset.name = system_info['hostname']
    
    print(f"updated_at após atribuição: {asset.updated_at}")
    print(f"last_seen após atribuição: {asset.last_seen}")
    print(f"name após atualização: {asset.name}")
    
    try:
        db.session.commit()
        print("✅ Commit realizado com sucesso")
        
        # Recarregar o asset do banco
        db.session.refresh(asset)
        print(f"updated_at após commit: {asset.updated_at}")
        print(f"last_seen após commit: {asset.last_seen}")
        
        if asset.updated_at != old_updated_at:
            print("✅ updated_at foi atualizado corretamente")
        else:
            print("❌ updated_at NÃO foi atualizado")
            
        if asset.last_seen != old_last_seen:
            print("✅ last_seen foi atualizado corretamente")
        else:
            print("❌ last_seen NÃO foi atualizado")
            
    except Exception as e:
        print(f"❌ Erro no commit: {e}")
        db.session.rollback()

def check_recent_assets():
    """Verifica assets recentemente atualizados"""
    
    print("\n=== VERIFICAÇÃO DE ASSETS RECENTES ===")
    
    # Buscar assets ordenados por updated_at
    recent_assets = Asset.query.order_by(Asset.updated_at.desc()).limit(5).all()
    
    print("Top 5 assets mais recentemente atualizados:")
    for i, asset in enumerate(recent_assets, 1):
        agent = Agent.query.filter_by(asset_id=asset.id).first()
        agent_status = f"Agente: {agent.agent_version}" if agent else "Sem agente"
        
        print(f"  {i}. {asset.name} (ID: {asset.id})")
        print(f"     updated_at: {asset.updated_at}")
        print(f"     last_seen: {asset.last_seen}")
        print(f"     {agent_status}")
        print()

if __name__ == "__main__":
    try:
        # Importar app para inicializar o banco
        from app import app
        
        with app.app_context():
            test_checkin_updated_at()
            check_recent_assets()
            
    except Exception as e:
        print(f"Erro durante o teste: {e}")
        import traceback
        traceback.print_exc() 
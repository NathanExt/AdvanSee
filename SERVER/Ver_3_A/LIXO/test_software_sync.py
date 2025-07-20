#!/usr/bin/env python3
"""
Script de teste para verificar a sincronização de software instalado
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import db, Asset, InstalledSoftware, Agent
from datetime import datetime

def test_software_sync():
    """Testa a sincronização de software para um asset específico"""
    
    # Buscar um asset que tenha agente
    asset = Asset.query.join(Agent).first()
    
    if not asset:
        print("Nenhum asset com agente encontrado para teste")
        return
    
    print(f"Testando sincronização para asset: {asset.name} (ID: {asset.id})")
    
    # Mostrar softwares atualmente no banco
    current_software = InstalledSoftware.query.filter_by(asset_id=asset.id).all()
    print(f"\nSoftwares atualmente no banco ({len(current_software)}):")
    for sw in current_software[:10]:  # Mostrar apenas os primeiros 10
        print(f"  - {sw.name} {sw.version} ({sw.vendor})")
    
    if len(current_software) > 10:
        print(f"  ... e mais {len(current_software) - 10} softwares")
    
    # Simular dados do agente (exemplo)
    agent_data = {
        'installed_software': [
            {'name': 'Google Chrome', 'version': '120.0.6099.109', 'vendor': 'Google LLC'},
            {'name': 'Mozilla Firefox', 'version': '121.0', 'vendor': 'Mozilla Corporation'},
            {'name': 'Microsoft Edge', 'version': '120.0.2210.91', 'vendor': 'Microsoft Corporation'},
            {'name': 'Visual Studio Code', 'version': '1.85.1', 'vendor': 'Microsoft Corporation'},
            {'name': 'Python', 'version': '3.11.0', 'vendor': 'Python Software Foundation'},
            # Adicionar alguns softwares que podem não estar no banco
            {'name': 'Notepad++', 'version': '8.6.2', 'vendor': 'Notepad++ Team'},
            {'name': '7-Zip', 'version': '23.01', 'vendor': 'Igor Pavlov'},
        ]
    }
    
    print(f"\nDados simulados do agente ({len(agent_data['installed_software'])} softwares):")
    for sw in agent_data['installed_software']:
        print(f"  - {sw['name']} {sw['version']} ({sw['vendor']})")
    
    # Simular a lógica de sincronização
    print(f"\n=== SIMULAÇÃO DA SINCRONIZAÇÃO ===")
    
    # 1. Obter softwares atualmente no banco
    current_software_in_db = InstalledSoftware.query.filter_by(asset_id=asset.id).all()
    current_software_set = set()
    
    for sw in current_software_in_db:
        key = f"{sw.name}|{sw.version or ''}|{sw.vendor or ''}"
        current_software_set.add(key)
    
    print(f"1. Softwares no banco: {len(current_software_set)}")
    
    # 2. Processar softwares do agente
    agent_software_set = set()
    software_to_insert = []
    software_removed_count = 0
    software_added_count = 0
    
    for software_data in agent_data['installed_software']:
        name = software_data.get('name')
        version = software_data.get('version')
        vendor = software_data.get('vendor')
        
        if name:
            key = f"{name}|{version or ''}|{vendor or ''}"
            agent_software_set.add(key)
            
            if key not in current_software_set:
                software_to_insert.append({
                    'asset_id': asset.id,
                    'name': name,
                    'version': version,
                    'vendor': vendor,
                    'created_at': datetime.utcnow()
                })
                software_added_count += 1
    
    print(f"2. Softwares do agente: {len(agent_software_set)}")
    print(f"3. Novos softwares para adicionar: {software_added_count}")
    
    # 3. Identificar softwares desinstalados
    software_to_remove = current_software_set - agent_software_set
    software_removed_list = []
    
    for sw in current_software_in_db:
        key = f"{sw.name}|{sw.version or ''}|{sw.vendor or ''}"
        if key in software_to_remove:
            software_removed_list.append(sw)
            software_removed_count += 1
    
    print(f"4. Softwares para remover (desinstalados): {software_removed_count}")
    
    if software_removed_list:
        print("   Softwares que seriam removidos:")
        for sw in software_removed_list[:5]:
            print(f"     - {sw.name} {sw.version}")
        if len(software_removed_list) > 5:
            print(f"     ... e mais {len(software_removed_list) - 5}")
    
    if software_to_insert:
        print("   Novos softwares que seriam adicionados:")
        for sw in software_to_insert:
            print(f"     - {sw['name']} {sw['version']}")
    
    print(f"\n=== RESUMO ===")
    print(f"Total de mudanças: {software_added_count + software_removed_count}")
    print(f"Softwares adicionados: {software_added_count}")
    print(f"Softwares removidos: {software_removed_count}")
    print(f"Total final: {len(agent_software_set)}")

def check_software_consistency():
    """Verifica a consistência dos dados de software no banco"""
    
    print("=== VERIFICAÇÃO DE CONSISTÊNCIA ===")
    
    # Contar softwares por asset
    assets_with_software = db.session.query(
        Asset.id, 
        Asset.name, 
        db.func.count(InstalledSoftware.id).label('software_count')
    ).join(InstalledSoftware).group_by(Asset.id, Asset.name).all()
    
    print(f"Assets com software instalado: {len(assets_with_software)}")
    
    for asset_id, asset_name, software_count in assets_with_software:
        print(f"  - {asset_name} (ID: {asset_id}): {software_count} softwares")
    
    # Verificar softwares duplicados
    duplicates = db.session.query(
        InstalledSoftware.asset_id,
        InstalledSoftware.name,
        InstalledSoftware.version,
        InstalledSoftware.vendor,
        db.func.count(InstalledSoftware.id).label('count')
    ).group_by(
        InstalledSoftware.asset_id,
        InstalledSoftware.name,
        InstalledSoftware.version,
        InstalledSoftware.vendor
    ).having(db.func.count(InstalledSoftware.id) > 1).all()
    
    if duplicates:
        print(f"\nSoftwares duplicados encontrados: {len(duplicates)}")
        for dup in duplicates[:5]:
            print(f"  - Asset {dup.asset_id}: {dup.name} {dup.version} ({dup.count} vezes)")
    else:
        print("\nNenhum software duplicado encontrado")

if __name__ == "__main__":
    try:
        # Importar app para inicializar o banco
        from app import app
        
        with app.app_context():
            print("=== TESTE DE SINCRONIZAÇÃO DE SOFTWARE ===")
            test_software_sync()
            print("\n")
            check_software_consistency()
            
    except Exception as e:
        print(f"Erro durante o teste: {e}")
        import traceback
        traceback.print_exc() 
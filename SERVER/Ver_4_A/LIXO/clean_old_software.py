#!/usr/bin/env python3
"""
Script para limpar softwares antigos/desinstalados do banco de dados
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import db, Asset, InstalledSoftware, Agent, AssetHistory
from datetime import datetime, timedelta

def clean_old_software():
    """Remove softwares que não foram atualizados recentemente"""
    
    print("=== LIMPEZA DE SOFTWARES ANTIGOS ===")
    
    # Buscar assets com agente
    assets_with_agent = Asset.query.join(Agent).all()
    
    if not assets_with_agent:
        print("Nenhum asset com agente encontrado")
        return
    
    total_removed = 0
    
    for asset in assets_with_agent:
        print(f"\nProcessando asset: {asset.name} (ID: {asset.id})")
        
        # Buscar softwares deste asset
        software_list = InstalledSoftware.query.filter_by(asset_id=asset.id).all()
        
        if not software_list:
            print("  Nenhum software encontrado")
            continue
        
        print(f"  Softwares encontrados: {len(software_list)}")
        
        # Verificar último check-in do agente
        agent = Agent.query.filter_by(asset_id=asset.id).first()
        if not agent or not agent.last_checkin:
            print("  Agente sem último check-in - pulando")
            continue
        
        # Se o último check-in foi há mais de 30 dias, considerar softwares como desatualizados
        days_since_checkin = (datetime.utcnow() - agent.last_checkin).days
        
        if days_since_checkin > 30:
            print(f"  Último check-in há {days_since_checkin} dias - removendo todos os softwares")
            
            # Registrar no histórico
            history = AssetHistory(
                asset_id=asset.id,
                user_id=None,
                action='software_cleanup_old',
                new_value=f'Removidos {len(software_list)} softwares devido a check-in antigo ({days_since_checkin} dias)'
            )
            db.session.add(history)
            
            # Remover todos os softwares
            for sw in software_list:
                db.session.delete(sw)
            
            total_removed += len(software_list)
            print(f"  Removidos {len(software_list)} softwares")
        else:
            print(f"  Último check-in há {days_since_checkin} dias - mantendo softwares")
    
    # Commit das mudanças
    if total_removed > 0:
        db.session.commit()
        print(f"\n=== RESUMO ===")
        print(f"Total de softwares removidos: {total_removed}")
        print("Limpeza concluída com sucesso!")
    else:
        print(f"\nNenhum software foi removido")

def show_software_stats():
    """Mostra estatísticas dos softwares no banco"""
    
    print("=== ESTATÍSTICAS DE SOFTWARE ===")
    
    # Total de softwares
    total_software = InstalledSoftware.query.count()
    print(f"Total de softwares no banco: {total_software}")
    
    # Softwares por asset
    assets_with_software = db.session.query(
        Asset.id, 
        Asset.name, 
        db.func.count(InstalledSoftware.id).label('software_count')
    ).join(InstalledSoftware).group_by(Asset.id, Asset.name).all()
    
    print(f"Assets com software: {len(assets_with_software)}")
    
    if assets_with_software:
        print("\nTop 10 assets com mais softwares:")
        sorted_assets = sorted(assets_with_software, key=lambda x: x.software_count, reverse=True)
        
        for i, (asset_id, asset_name, software_count) in enumerate(sorted_assets[:10], 1):
            print(f"  {i}. {asset_name} (ID: {asset_id}): {software_count} softwares")
    
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
        print(f"\nSoftwares duplicados: {len(duplicates)}")
        for dup in duplicates[:5]:
            print(f"  - Asset {dup.asset_id}: {dup.name} {dup.version} ({dup.count} vezes)")
    else:
        print("\nNenhum software duplicado encontrado")

def interactive_cleanup():
    """Limpeza interativa - permite escolher quais softwares remover"""
    
    print("=== LIMPEZA INTERATIVA ===")
    
    # Buscar assets com software
    assets_with_software = db.session.query(
        Asset.id, 
        Asset.name, 
        db.func.count(InstalledSoftware.id).label('software_count')
    ).join(InstalledSoftware).group_by(Asset.id, Asset.name).order_by(db.func.count(InstalledSoftware.id).desc()).all()
    
    if not assets_with_software:
        print("Nenhum asset com software encontrado")
        return
    
    print("Assets com software:")
    for i, (asset_id, asset_name, software_count) in enumerate(assets_with_software, 1):
        print(f"  {i}. {asset_name} (ID: {asset_id}): {software_count} softwares")
    
    try:
        choice = input("\nEscolha o número do asset para limpar (ou 'q' para sair): ")
        
        if choice.lower() == 'q':
            return
        
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(assets_with_software):
            asset_id, asset_name, software_count = assets_with_software[choice_idx]
            
            print(f"\nLimpando softwares do asset: {asset_name}")
            
            # Buscar softwares
            software_list = InstalledSoftware.query.filter_by(asset_id=asset_id).all()
            
            print(f"Softwares encontrados ({len(software_list)}):")
            for i, sw in enumerate(software_list[:20], 1):
                print(f"  {i}. {sw.name} {sw.version} ({sw.vendor})")
            
            if len(software_list) > 20:
                print(f"  ... e mais {len(software_list) - 20} softwares")
            
            confirm = input(f"\nRemover todos os {len(software_list)} softwares? (s/n): ")
            
            if confirm.lower() == 's':
                # Registrar no histórico
                history = AssetHistory(
                    asset_id=asset_id,
                    user_id=None,
                    action='software_cleanup_manual',
                    new_value=f'Removidos {len(software_list)} softwares manualmente'
                )
                db.session.add(history)
                
                # Remover softwares
                for sw in software_list:
                    db.session.delete(sw)
                
                db.session.commit()
                print(f"Removidos {len(software_list)} softwares com sucesso!")
            else:
                print("Operação cancelada")
        else:
            print("Escolha inválida")
            
    except (ValueError, KeyboardInterrupt):
        print("Operação cancelada")

if __name__ == "__main__":
    try:
        # Importar app para inicializar o banco
        from app import app
        
        with app.app_context():
            print("=== FERRAMENTA DE LIMPEZA DE SOFTWARE ===")
            print("1. Mostrar estatísticas")
            print("2. Limpeza automática (softwares antigos)")
            print("3. Limpeza interativa")
            print("4. Sair")
            
            choice = input("\nEscolha uma opção (1-4): ")
            
            if choice == "1":
                show_software_stats()
            elif choice == "2":
                clean_old_software()
            elif choice == "3":
                interactive_cleanup()
            elif choice == "4":
                print("Saindo...")
            else:
                print("Opção inválida")
            
    except Exception as e:
        print(f"Erro durante a execução: {e}")
        import traceback
        traceback.print_exc() 
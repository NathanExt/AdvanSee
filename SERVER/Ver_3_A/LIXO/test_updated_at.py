#!/usr/bin/env python3
"""
Script para testar a atualização da coluna updated_at
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import db, Asset, Agent
from datetime import datetime
import time

def test_updated_at():
    """Testa a atualização da coluna updated_at"""
    
    print("=== TESTE DE ATUALIZAÇÃO DA COLUNA updated_at ===")
    
    # Buscar um asset com agente
    asset = Asset.query.join(Agent).first()
    
    if not asset:
        print("Nenhum asset com agente encontrado para teste")
        return
    
    print(f"Asset: {asset.name} (ID: {asset.id})")
    print(f"updated_at atual: {asset.updated_at}")
    print(f"last_seen atual: {asset.last_seen}")
    
    # Verificar se o modelo tem a coluna updated_at
    if hasattr(asset, 'updated_at'):
        print("✅ Coluna updated_at existe no modelo")
    else:
        print("❌ Coluna updated_at NÃO existe no modelo")
        return
    
    # Verificar se a coluna tem onupdate configurado
    try:
        column = Asset.__table__.columns.get('updated_at')
        if column is not None and hasattr(column, 'onupdate'):
            print(f"✅ Coluna updated_at tem onupdate: {column.onupdate}")
        else:
            print("❌ Coluna updated_at NÃO tem onupdate configurado")
    except Exception as e:
        print(f"❌ Erro ao verificar coluna: {e}")
    
    # Testar atualização manual
    print("\n--- Teste 1: Atualização manual ---")
    old_updated_at = asset.updated_at
    print(f"updated_at antes: {old_updated_at}")
    
    # Aguardar 1 segundo para garantir diferença
    time.sleep(1)
    
    # Atualizar manualmente
    asset.updated_at = datetime.utcnow()
    asset.last_seen = datetime.utcnow()
    
    print(f"updated_at após atribuição: {asset.updated_at}")
    
    # Commit para ver se funciona
    try:
        db.session.commit()
        print("✅ Commit realizado com sucesso")
        
        # Recarregar o asset do banco
        db.session.refresh(asset)
        print(f"updated_at após commit: {asset.updated_at}")
        
        if asset.updated_at != old_updated_at:
            print("✅ updated_at foi atualizado no banco")
        else:
            print("❌ updated_at NÃO foi atualizado no banco")
            
    except Exception as e:
        print(f"❌ Erro no commit: {e}")
        db.session.rollback()
    
    # Testar atualização via SQLAlchemy onupdate
    print("\n--- Teste 2: Atualização via onupdate ---")
    
    # Aguardar 1 segundo
    time.sleep(1)
    
    # Modificar um campo para trigger o onupdate
    old_updated_at = asset.updated_at
    print(f"updated_at antes da modificação: {old_updated_at}")
    
    # Modificar um campo simples
    asset.name = asset.name  # Mesmo valor, mas pode trigger o onupdate
    
    try:
        db.session.commit()
        print("✅ Commit realizado com sucesso")
        
        # Recarregar o asset do banco
        db.session.refresh(asset)
        print(f"updated_at após commit: {asset.updated_at}")
        
        if asset.updated_at != old_updated_at:
            print("✅ onupdate funcionou - updated_at foi atualizado")
        else:
            print("❌ onupdate NÃO funcionou - updated_at não foi atualizado")
            
    except Exception as e:
        print(f"❌ Erro no commit: {e}")
        db.session.rollback()
    
    # Testar modificação real de um campo
    print("\n--- Teste 3: Modificação real de campo ---")
    
    # Aguardar 1 segundo
    time.sleep(1)
    
    old_updated_at = asset.updated_at
    old_description = asset.description
    print(f"updated_at antes da modificação: {old_updated_at}")
    
    # Modificar um campo real
    asset.description = f"Teste de atualização - {datetime.utcnow()}"
    
    try:
        db.session.commit()
        print("✅ Commit realizado com sucesso")
        
        # Recarregar o asset do banco
        db.session.refresh(asset)
        print(f"updated_at após commit: {asset.updated_at}")
        print(f"description após commit: {asset.description}")
        
        if asset.updated_at != old_updated_at:
            print("✅ onupdate funcionou com modificação real")
        else:
            print("❌ onupdate NÃO funcionou mesmo com modificação real")
            
        # Restaurar description original
        asset.description = old_description
        db.session.commit()
        
    except Exception as e:
        print(f"❌ Erro no commit: {e}")
        db.session.rollback()

def check_database_schema():
    """Verifica o schema da tabela assets no banco"""
    
    print("\n=== VERIFICAÇÃO DO SCHEMA DA TABELA ===")
    
    try:
        # Verificar se a coluna updated_at existe na tabela
        result = db.session.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'assets' AND column_name = 'updated_at'
        """).fetchone()
        
        if result:
            print(f"✅ Coluna updated_at encontrada na tabela:")
            print(f"   Nome: {result[0]}")
            print(f"   Tipo: {result[1]}")
            print(f"   Nullable: {result[2]}")
            print(f"   Default: {result[3]}")
        else:
            print("❌ Coluna updated_at NÃO encontrada na tabela")
            
        # Verificar triggers ou constraints
        result = db.session.execute("""
            SELECT trigger_name, event_manipulation, action_statement
            FROM information_schema.triggers 
            WHERE event_object_table = 'assets'
        """).fetchall()
        
        if result:
            print(f"\nTriggers encontrados na tabela assets:")
            for trigger in result:
                print(f"   {trigger[0]}: {trigger[1]} - {trigger[2]}")
        else:
            print("\nNenhum trigger encontrado na tabela assets")
            
    except Exception as e:
        print(f"❌ Erro ao verificar schema: {e}")

def simulate_agent_checkin():
    """Simula um checkin de agente para testar updated_at"""
    
    print("\n=== SIMULAÇÃO DE CHECKIN DE AGENTE ===")
    
    # Buscar um asset com agente
    asset = Asset.query.join(Agent).first()
    
    if not asset:
        print("Nenhum asset com agente encontrado para teste")
        return
    
    print(f"Asset: {asset.name} (ID: {asset.id})")
    print(f"updated_at antes do checkin: {asset.updated_at}")
    
    # Simular o que acontece no checkin
    old_updated_at = asset.updated_at
    
    # Aguardar 1 segundo
    time.sleep(1)
    
    # Atualizar campos como no checkin real
    asset.last_seen = datetime.utcnow()
    asset.updated_at = datetime.utcnow()  # Linha 175 do código original
    
    print(f"updated_at após atribuição: {asset.updated_at}")
    
    try:
        db.session.commit()
        print("✅ Commit realizado com sucesso")
        
        # Recarregar o asset do banco
        db.session.refresh(asset)
        print(f"updated_at após commit: {asset.updated_at}")
        
        if asset.updated_at != old_updated_at:
            print("✅ updated_at foi atualizado corretamente")
        else:
            print("❌ updated_at NÃO foi atualizado")
            
    except Exception as e:
        print(f"❌ Erro no commit: {e}")
        db.session.rollback()

if __name__ == "__main__":
    try:
        # Importar app para inicializar o banco
        from app import app
        
        with app.app_context():
            test_updated_at()
            check_database_schema()
            simulate_agent_checkin()
            
    except Exception as e:
        print(f"Erro durante o teste: {e}")
        import traceback
        traceback.print_exc() 
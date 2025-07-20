#!/usr/bin/env python3
"""
Script de teste para a função sync_pmoc_assets_2
"""

import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modulos.pmoc.pmoc_assets import sync_pmoc_assets_2
from models.database import db, Asset, PmocAsset

def test_sync_pmoc_assets_2():
    """
    Testa a função sync_pmoc_assets_2
    """
    print("=== Teste da função sync_pmoc_assets_2 ===")
    
    try:
        # Verificar assets existentes
        total_assets = Asset.query.count()
        print(f"Total de assets no banco: {total_assets}")
        
        # Verificar registros PMOC existentes
        total_pmoc = PmocAsset.query.count()
        print(f"Total de registros PMOC existentes: {total_pmoc}")
        
        # Executar sincronização
        print("\nExecutando sincronização...")
        stats = sync_pmoc_assets_2()
        
        # Exibir resultados
        print("\n=== Resultados da Sincronização ===")
        print(f"Assets processados: {stats.get('assets_processed', 0)}")
        print(f"Assets com correspondência: {stats.get('assets_matched', 0)}")
        print(f"Registros criados: {stats.get('assets_created', 0)}")
        print(f"Registros atualizados: {stats.get('assets_updated', 0)}")
        print(f"Erros: {len(stats.get('errors', []))}")
        
        # Exibir erros se houver
        if stats.get('errors'):
            print("\n=== Erros Encontrados ===")
            for error in stats['errors']:
                print(f"- {error}")
        
        # Verificar registros PMOC após sincronização
        total_pmoc_after = PmocAsset.query.count()
        print(f"\nTotal de registros PMOC após sincronização: {total_pmoc_after}")
        print(f"Novos registros criados: {total_pmoc_after - total_pmoc}")
        
        # Mostrar alguns exemplos de registros criados
        if total_pmoc_after > total_pmoc:
            print("\n=== Exemplos de Registros Criados ===")
            new_records = PmocAsset.query.order_by(PmocAsset.id.desc()).limit(5).all()
            for record in new_records:
                asset = Asset.query.get(record.asset_id)
                print(f"Asset: {asset.name if asset else 'N/A'} -> PMOC: {record.pmoc_type} - {record.tag}")
        
        return True
        
    except Exception as e:
        print(f"Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_individual_asset():
    """
    Testa a busca de um asset individual
    """
    print("\n=== Teste de Asset Individual ===")
    
    try:
        from modulos.pmoc.pmoc_search import PMOCSearch
        
        # Buscar um asset que tenha nome ou tag
        asset = Asset.query.filter(
            (Asset.name.isnot(None)) | (Asset.tag.isnot(None)) | (Asset.asset_tag.isnot(None))
        ).first()
        
        if not asset:
            print("Nenhum asset encontrado para teste")
            return False
        
        print(f"Testando asset: ID={asset.id}, Nome={asset.name}, Tag={asset.tag}")
        
        searcher = PMOCSearch()
        try:
            results = searcher.search_asset_by_hostname_and_tag(asset.name or '', asset.tag or asset.asset_tag or '')
            print(f"Resultados encontrados: {results.get('total_found', 0)}")
            
            if results.get('notebooks'):
                print(f"Notebooks: {len(results['notebooks'])}")
                for nb in results['notebooks'][:2]:  # Mostrar apenas os 2 primeiros
                    print(f"  - {nb.get('patrimony')} ({nb.get('manufacturer')} {nb.get('model')})")
            
            if results.get('desktops'):
                print(f"Desktops: {len(results['desktops'])}")
                for dt in results['desktops'][:2]:  # Mostrar apenas os 2 primeiros
                    print(f"  - {dt.get('patrimony')} ({dt.get('manufacturer')} {dt.get('model')})")
            
            return True
            
        finally:
            searcher.close()
            
    except Exception as e:
        print(f"Erro durante o teste individual: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Iniciando testes da sincronização PMOC V2...")
    
    # Teste individual primeiro
    test_individual_asset()
    
    # Teste da sincronização completa
    success = test_sync_pmoc_assets_2()
    
    if success:
        print("\n✅ Todos os testes concluídos com sucesso!")
    else:
        print("\n❌ Alguns testes falharam!")
        sys.exit(1) 
import requests
from models.database import db, PmocAsset, Asset
from sqlalchemy import or_
from datetime import datetime
from modulos.pmoc.pmoc_search import search_pmoc_asset, PMOCSearch


#Busca os dados dos notebooks no firebase
def notebook():
    url = 'https://sensedia.uisa.com.br/app-equipment/api/v1/firebase/get?environment=prd&type=notebook'

    try:
        response = requests.get(url)
        response.raise_for_status()  # lança exceção para status 4xx/5xx

        dados = response.json()
        if isinstance(dados, list):
            return dados
        else:
            print("Resposta não é uma lista:", type(dados))
            return []


    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return []

#Busca os dados dos desktops no firebase
def desktop():
    url = 'https://sensedia.uisa.com.br/app-equipment/api/v1/firebase/get?environment=prd&type=desktop'

    try:
        response = requests.get(url)
        response.raise_for_status()  # lança exceção para status 4xx/5xx

        dados = response.json()
        if isinstance(dados, list):
            return dados
        else:
            print("Resposta não é uma lista:", type(dados))
            return []

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return []

def sync_pmoc_assets():
    """
    Sincroniza os dados do PMOC com a tabela pmoc_assets
    Retorna um dicionário com estatísticas da sincronização
    """
    stats = {
        'notebooks_processed': 0,
        'desktops_processed': 0,
        'assets_matched': 0,
        'assets_created': 0,
        'assets_updated': 0,
        'errors': []
    }
    
    try:
        # Buscar dados do PMOC
        notebooks_data = notebook()
        desktops_data = desktop()
        
        # Processar notebooks
        for notebook in notebooks_data:
            stats['notebooks_processed'] += 1
            try:
                _process_pmoc_item(notebook, 'notebook', stats)
            except Exception as e:
                stats['errors'].append(f"Erro ao processar notebook {notebook.get('id', 'N/A')}: {str(e)}")
        
        # Processar desktops
        for desktop in desktops_data:
            stats['desktops_processed'] += 1
            try:
                _process_pmoc_item(desktop, 'desktop', stats)
            except Exception as e:
                stats['errors'].append(f"Erro ao processar desktop {desktop.get('id', 'N/A')}: {str(e)}")
        
        # Commit das mudanças
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        stats['errors'].append(f"Erro geral na sincronização: {str(e)}")
    
    return stats

def _process_pmoc_item(pmoc_item, pmoc_type, stats):
    """
    Processa um item individual do PMOC
    """
    pmoc_id = str(pmoc_item.get('id', ''))
    tag = pmoc_item.get('tag', '')
    tag_uisa = pmoc_item.get('tag_uisa', '')
    patrimony = pmoc_item.get('patrimony', '')
    
    # Tentar encontrar asset correspondente
    asset = None
    
    # Buscar por tag
    if tag:
        asset = Asset.query.filter(
            or_(
                Asset.tag == tag,
                Asset.asset_tag == tag
            )
        ).first()
    
    # Buscar por tag_uisa
    if not asset and tag_uisa:
        asset = Asset.query.filter(
            or_(
                Asset.tag == tag_uisa,
                Asset.asset_tag == tag_uisa
            )
        ).first()
    
    # Buscar por patrimony (nome do asset)
    if not asset and patrimony:
        asset = Asset.query.filter(Asset.name == patrimony).first()
    print(asset)
    if asset:
        stats['assets_matched'] += 1
        
        # Verificar se já existe registro PMOC para este asset
        existing_pmoc = PmocAsset.query.filter_by(
            asset_id=asset.id,
            pmoc_type=pmoc_type,
            pmoc_id=pmoc_id
        ).first()
        
        if existing_pmoc:
            # Atualizar registro existente
            existing_pmoc.tag = tag
            existing_pmoc.tag_uisa = tag_uisa
            existing_pmoc.patrimony = patrimony
            existing_pmoc.manufacturer = pmoc_item.get('manufacturer', '')
            existing_pmoc.model = pmoc_item.get('model', '')
            existing_pmoc.serial_number = pmoc_item.get('serial_number', '')
            existing_pmoc.user_name = pmoc_item.get('user_name', '')
            existing_pmoc.department = pmoc_item.get('department', '')
            existing_pmoc.location = pmoc_item.get('location', '')
            existing_pmoc.status = pmoc_item.get('status', '')
            existing_pmoc.last_sync = datetime.utcnow()
            stats['assets_updated'] += 1
        else:
            # Criar novo registro
            new_pmoc = PmocAsset(
                asset_id=asset.id,
                pmoc_type=pmoc_type,
                pmoc_id=pmoc_id,
                tag=tag,
                tag_uisa=tag_uisa,
                patrimony=patrimony,
                manufacturer=pmoc_item.get('manufacturer', ''),
                model=pmoc_item.get('model', ''),
                serial_number=pmoc_item.get('serial_number', ''),
                user_name=pmoc_item.get('user_name', ''),
                department=pmoc_item.get('department', ''),
                location=pmoc_item.get('location', ''),
                status=pmoc_item.get('status', ''),
                last_sync=datetime.utcnow()
            )
            db.session.add(new_pmoc)
            stats['assets_created'] += 1


def sync_pmoc_assets_2():
    """
    Sincroniza os dados do PMOC com a tabela pmoc_assets usando a classe PMOCSearch
    Esta versão usa busca direta no banco PMOC em vez da API
    """
    stats = {
        'assets_processed': 0,
        'assets_matched': 0,
        'assets_created': 0,
        'assets_updated': 0,
        'errors': []
    }
    
    searcher = PMOCSearch()
    
    try:
        # Buscar todos os assets que têm nome ou tag
        assets_to_sync = Asset.query.filter(
            or_(
                Asset.name.isnot(None),
                Asset.tag.isnot(None),
                Asset.asset_tag.isnot(None)
            )
        ).all()
        
        print(f"Processando {len(assets_to_sync)} assets para sincronização...")
        
        for asset in assets_to_sync:
            stats['assets_processed'] += 1
            
            try:
                # Buscar no PMOC usando hostname (nome) e tag
                hostname = asset.name or ''
                tag = asset.tag or asset.asset_tag or ''
                
                if not hostname and not tag:
                    continue
                
                print(f"Processando asset ID {asset.id}: {hostname} (tag: {tag})")
                
                # Buscar no PMOC
                results = searcher.search_asset_by_hostname_and_tag(hostname, tag)
                
                if 'error' in results:
                    stats['errors'].append(f"Asset {asset.id}: {results['error']}")
                    continue
                
                # Processar resultados de notebooks
                for notebook_data in results.get('notebooks', []):
                    _process_pmoc_result(asset, notebook_data, 'notebook', stats)
                
                # Processar resultados de desktops
                for desktop_data in results.get('desktops', []):
                    _process_pmoc_result(asset, desktop_data, 'desktop', stats)
                
                if results.get('total_found', 0) > 0:
                    stats['assets_matched'] += 1
                
            except Exception as e:
                error_msg = f"Erro ao processar asset {asset.id}: {str(e)}"
                stats['errors'].append(error_msg)
                print(error_msg)
        
        # Commit das mudanças
        db.session.commit()
        
        print(f"Sincronização concluída:")
        print(f"- Assets processados: {stats['assets_processed']}")
        print(f"- Assets com correspondência: {stats['assets_matched']}")
        print(f"- Registros criados: {stats['assets_created']}")
        print(f"- Registros atualizados: {stats['assets_updated']}")
        print(f"- Erros: {len(stats['errors'])}")
        
    except Exception as e:
        db.session.rollback()
        stats['errors'].append(f"Erro geral na sincronização: {str(e)}")
        print(f"Erro geral: {e}")
    
    finally:
        searcher.close()
    
    return stats


def _process_pmoc_result(asset, pmoc_data, pmoc_type, stats):
    """
    Processa um resultado individual do PMOC e salva na tabela pmoc_assets
    """
    pmoc_id = str(pmoc_data.get('id', ''))
    
    # Verificar se já existe registro PMOC para este asset
    existing_pmoc = PmocAsset.query.filter_by(
        asset_id=asset.id,
        pmoc_type=pmoc_type,
        pmoc_id=pmoc_id
    ).first()
    
    if existing_pmoc:
        # Atualizar registro existente
        existing_pmoc.tag = pmoc_data.get('tag', '')
        existing_pmoc.tag_uisa = pmoc_data.get('tag_uisa', '')
        existing_pmoc.patrimony = pmoc_data.get('patrimony', '')
        existing_pmoc.manufacturer = pmoc_data.get('manufacturer', '')
        existing_pmoc.model = pmoc_data.get('model', '')
        existing_pmoc.serial_number = pmoc_data.get('serial_number', '')
        existing_pmoc.user_name = pmoc_data.get('owner', '')
        existing_pmoc.department = pmoc_data.get('department', '')
        existing_pmoc.location = pmoc_data.get('location', '')
        existing_pmoc.status = pmoc_data.get('status', '')
        existing_pmoc.last_sync = datetime.utcnow()
        stats['assets_updated'] += 1
    else:
        # Criar novo registro
        new_pmoc = PmocAsset(
            asset_id=asset.id,
            pmoc_type=pmoc_type,
            pmoc_id=pmoc_id,
            tag=pmoc_data.get('tag', ''),
            tag_uisa=pmoc_data.get('tag_uisa', ''),
            patrimony=pmoc_data.get('patrimony', ''),
            manufacturer=pmoc_data.get('manufacturer', ''),
            model=pmoc_data.get('model', ''),
            serial_number=pmoc_data.get('serial_number', ''),
            user_name=pmoc_data.get('owner', ''),
            department=pmoc_data.get('department', ''),
            location=pmoc_data.get('location', ''),
            status=pmoc_data.get('status', ''),
            last_sync=datetime.utcnow()
        )
        db.session.add(new_pmoc)
        stats['assets_created'] += 1


from flask import Blueprint, render_template, request, jsonify
from models.database import db, Asset
from modulos.pmoc.pmoc_models.pmoc_database import Notebook, Desktop
from sqlalchemy import func, or_

bp_assets = Blueprint('assets', __name__)

@bp_assets.route('/assets')
def assets():
    # Parâmetros de busca
    search_name = request.args.get('search_name', '')
    search_manufacturer = request.args.get('search_manufacturer', '')
    search_model = request.args.get('search_model', '')
    search_user = request.args.get('search_user', '')
    search_status = request.args.get('search_status', '')
    
    # Query base para assets
    assets_query = Asset.query
    
    # Aplicar filtros de busca
    if search_name:
        assets_query = assets_query.filter(
            or_(
                Asset.name.ilike(f'%{search_name}%'),
                Asset.asset_tag.ilike(f'%{search_name}%')
            )
        )
    if search_manufacturer:
        assets_query = assets_query.filter(Asset.computer_manufacturer.ilike(f'%{search_manufacturer}%'))
    if search_model:
        assets_query = assets_query.filter(Asset.computer_model.ilike(f'%{search_model}%'))
    if search_user:
        assets_query = assets_query.filter(Asset.logged_user.ilike(f'%{search_user}%'))
    if search_status:
        assets_query = assets_query.filter(Asset.status.ilike(f'%{search_status}%'))
    
    # Obter lista de assets filtrada
    assets = assets_query.all()
    
    # Estatísticas gerais
    total_assets = Asset.query.count()
    total_notebooks_pmoc = Notebook.query.count()
    total_desktops_pmoc = Desktop.query.count()
    total_pmoc = total_notebooks_pmoc + total_desktops_pmoc
    
    # Contar assets encontrados no PMOC (usando a nova tabela pmoc_assets)
    from models.database import PmocAsset
    assets_found_in_pmoc = PmocAsset.query.count()
    
    # Dados para gráficos
    # Equipamentos por fabricante
    manufacturer_data = db.session.query(
        Asset.computer_manufacturer,
        func.count(Asset.id).label('count')
    ).filter(Asset.computer_manufacturer.isnot(None)).group_by(Asset.computer_manufacturer).order_by(func.count(Asset.id).desc()).limit(10).all()
    
    # Equipamentos por modelo
    model_data = db.session.query(
        Asset.computer_model,
        func.count(Asset.id).label('count')
    ).filter(Asset.computer_model.isnot(None)).group_by(Asset.computer_model).order_by(func.count(Asset.id).desc()).limit(10).all()
    
    # Status dos equipamentos
    status_data = db.session.query(
        Asset.status,
        func.count(Asset.id).label('count')
    ).group_by(Asset.status).order_by(func.count(Asset.id).desc()).all()
    
    # Equipamentos PMOC por fabricante
    pmoc_manufacturer_data = []
    try:
        notebook_manufacturers = db.session.query(
            Notebook.manufacturer,
            func.count(Notebook.id).label('count')
        ).filter(Notebook.manufacturer.isnot(None)).group_by(Notebook.manufacturer).all()
        
        desktop_manufacturers = db.session.query(
            Desktop.manufacturer,
            func.count(Desktop.id).label('count')
        ).filter(Desktop.manufacturer.isnot(None)).group_by(Desktop.manufacturer).all()
        
        # Combinar dados de notebooks e desktops
        manufacturer_dict = {}
        for manufacturer, count in notebook_manufacturers:
            manufacturer_dict[manufacturer] = manufacturer_dict.get(manufacturer, 0) + count
        
        for manufacturer, count in desktop_manufacturers:
            manufacturer_dict[manufacturer] = manufacturer_dict.get(manufacturer, 0) + count
        
        # Converter para lista ordenada
        pmoc_manufacturer_data = sorted(manufacturer_dict.items(), key=lambda x: x[1], reverse=True)[:10]
    except Exception as e:
        print(f"Erro ao buscar dados PMOC: {e}")
    
    # Preparar dados para gráficos em formato JSON
    chart_data = {
        'manufacturers': {
            'labels': [item[0] if item[0] else 'N/A' for item in manufacturer_data],
            'data': [item[1] for item in manufacturer_data]
        },
        'models': {
            'labels': [item[0] if item[0] else 'N/A' for item in model_data],
            'data': [item[1] for item in model_data]
        },
        'status': {
            'labels': [item[0] if item[0] else 'N/A' for item in status_data],
            'data': [item[1] for item in status_data]
        },
        'pmoc_manufacturers': {
            'labels': [item[0] if item[0] else 'N/A' for item in pmoc_manufacturer_data],
            'data': [item[1] for item in pmoc_manufacturer_data]
        }
    }
    
    # Obter listas de valores únicos para filtros
    manufacturers = db.session.query(Asset.computer_manufacturer).filter(Asset.computer_manufacturer.isnot(None)).distinct().order_by(Asset.computer_manufacturer).all()
    models = db.session.query(Asset.computer_model).filter(Asset.computer_model.isnot(None)).distinct().order_by(Asset.computer_model).all()
    statuses = db.session.query(Asset.status).distinct().order_by(Asset.status).all()
    
    return render_template('assets.html', 
                         assets=assets,
                         total_assets=total_assets,
                         total_pmoc=total_pmoc,
                         total_notebooks_pmoc=total_notebooks_pmoc,
                         total_desktops_pmoc=total_desktops_pmoc,
                         assets_found_in_pmoc=assets_found_in_pmoc,
                         chart_data=chart_data,
                         manufacturers=[m[0] for m in manufacturers],
                         models=[m[0] for m in models],
                         statuses=[s[0] for s in statuses],
                         search_name=search_name,
                         search_manufacturer=search_manufacturer,
                         search_model=search_model,
                         search_user=search_user,
                         search_status=search_status)

@bp_assets.route('/assets/api/search')
def assets_api_search():
    """API endpoint para busca de assets via AJAX"""
    search_name = request.args.get('search_name', '')
    search_manufacturer = request.args.get('search_manufacturer', '')
    search_model = request.args.get('search_model', '')
    search_user = request.args.get('search_user', '')
    search_status = request.args.get('search_status', '')
    
    # Query base para assets
    assets_query = Asset.query
    
    # Aplicar filtros de busca
    if search_name:
        assets_query = assets_query.filter(
            or_(
                Asset.name.ilike(f'%{search_name}%'),
                Asset.asset_tag.ilike(f'%{search_name}%')
            )
        )
    if search_manufacturer:
        assets_query = assets_query.filter(Asset.computer_manufacturer.ilike(f'%{search_manufacturer}%'))
    if search_model:
        assets_query = assets_query.filter(Asset.computer_model.ilike(f'%{search_model}%'))
    if search_user:
        assets_query = assets_query.filter(Asset.logged_user.ilike(f'%{search_user}%'))
    if search_status:
        assets_query = assets_query.filter(Asset.status.ilike(f'%{search_status}%'))
    
    # Obter lista de assets filtrada
    assets = assets_query.all()
    
    # Preparar dados para retorno JSON
    assets_data = []
    for asset in assets:
        assets_data.append({
            'id': asset.id,
            'asset_tag': asset.asset_tag,
            'name': asset.name,
            'computer_model': asset.computer_model,
            'computer_manufacturer': asset.computer_manufacturer,
            'logged_user': asset.logged_user,
            'status': asset.status
        })
    
    return jsonify({
        'success': True,
        'assets': assets_data,
        'total': len(assets_data)
    })

@bp_assets.route('/assets/sync-pmoc', methods=['POST'])
def sync_pmoc():
    """Sincroniza os dados do PMOC com a tabela pmoc_assets"""
    try:
        from modulos.pmoc.pmoc_assets import sync_pmoc_assets
        
        # Executar sincronização
        stats = sync_pmoc_assets()
        
        return jsonify({
            'success': True,
            'message': 'Sincronização concluída com sucesso!',
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro durante a sincronização: {str(e)}',
            'stats': {}
        }), 500


@bp_assets.route('/assets/sync-pmoc-v2', methods=['POST'])
def sync_pmoc_v2():
    """Sincroniza os dados do PMOC com a tabela pmoc_assets usando busca direta no banco"""
    try:
        from modulos.pmoc.pmoc_assets import sync_pmoc_assets_2
        
        # Executar sincronização versão 2
        stats = sync_pmoc_assets_2()
        
        return jsonify({
            'success': True,
            'message': 'Sincronização V2 concluída com sucesso!',
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro durante a sincronização V2: {str(e)}',
            'stats': {}
        }), 500



from flask import Blueprint, render_template, request, jsonify
from models.database import db, Asset, AssetGroup, AssetGroupItem
from modulos.pmoc.pmoc_models.pmoc_database import Notebook, Desktop
from sqlalchemy import func, or_, and_
from datetime import datetime, timedelta
import json

bp_assets = Blueprint('assets', __name__)

@bp_assets.route('/assets')
def assets():
    # Parâmetros de busca
    search_name = request.args.get('search_name', '')
    search_manufacturer = request.args.get('search_manufacturer', '')
    search_model = request.args.get('search_model', '')
    search_user = request.args.get('search_user', '')
    search_status = request.args.get('search_status', '')
    active_tab = request.args.get('tab', 'dashboard')
    
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
    assets_online = Asset.query.filter_by(status='active').count()
    assets_offline = Asset.query.filter_by(status='inactive').count()
    
    total_notebooks_pmoc = Notebook.query.count()
    total_desktops_pmoc = Desktop.query.count()
    total_pmoc = total_notebooks_pmoc + total_desktops_pmoc
    
    # Contar assets encontrados no PMOC (usando a nova tabela pmoc_assets)
    from models.database import PmocAsset
    assets_found_in_pmoc = PmocAsset.query.count()
    
    # Obter grupos de assets
    asset_groups = AssetGroup.query.filter_by(is_active=True).all()
    
    # Dados para gráficos do Dashboard
    chart_data = get_dashboard_chart_data()
    
    # Obter listas de valores únicos para filtros
    manufacturers = db.session.query(Asset.computer_manufacturer).filter(
        Asset.computer_manufacturer.isnot(None)
    ).distinct().order_by(Asset.computer_manufacturer).all()
    
    models = db.session.query(Asset.computer_model).filter(
        Asset.computer_model.isnot(None)
    ).distinct().order_by(Asset.computer_model).all()
    
    statuses = db.session.query(Asset.status).distinct().order_by(Asset.status).all()
    
    return render_template('assets.html', 
                         assets=assets,
                         total_assets=total_assets,
                         assets_online=assets_online,
                         assets_offline=assets_offline,
                         total_pmoc=total_pmoc,
                         total_notebooks_pmoc=total_notebooks_pmoc,
                         total_desktops_pmoc=total_desktops_pmoc,
                         assets_found_in_pmoc=assets_found_in_pmoc,
                         asset_groups=asset_groups,
                         chart_data=chart_data,
                         manufacturers=[m[0] for m in manufacturers],
                         models=[m[0] for m in models],
                         statuses=[s[0] for s in statuses],
                         search_name=search_name,
                         search_manufacturer=search_manufacturer,
                         search_model=search_model,
                         search_user=search_user,
                         search_status=search_status,
                         active_tab=active_tab)

def get_dashboard_chart_data():
    """Gera dados para os gráficos do dashboard"""
    
    # Status dos equipamentos
    status_data = db.session.query(
        Asset.status,
        func.count(Asset.id).label('count')
    ).group_by(Asset.status).order_by(func.count(Asset.id).desc()).all()
    
    # Sistemas Operacionais
    os_data = db.session.query(
        Asset.operating_system,
        func.count(Asset.id).label('count')
    ).filter(Asset.operating_system.isnot(None)).group_by(
        Asset.operating_system
    ).order_by(func.count(Asset.id).desc()).limit(10).all()
    
    # Equipamentos por fabricante
    manufacturer_data = db.session.query(
        Asset.computer_manufacturer,
        func.count(Asset.id).label('count')
    ).filter(Asset.computer_manufacturer.isnot(None)).group_by(
        Asset.computer_manufacturer
    ).order_by(func.count(Asset.id).desc()).limit(10).all()
    
    # Equipamentos por modelo
    model_data = db.session.query(
        Asset.computer_model,
        func.count(Asset.id).label('count')
    ).filter(Asset.computer_model.isnot(None)).group_by(
        Asset.computer_model
    ).order_by(func.count(Asset.id).desc()).limit(10).all()
    
    # Assets por departamento (usando logged_user como proxy)
    # PostgreSQL usa split_part em vez de substring_index
    department_data = db.session.query(
        func.split_part(Asset.logged_user, '@', 1).label('department'),
        func.count(Asset.id).label('count')
    ).filter(Asset.logged_user.isnot(None)).group_by(
        func.split_part(Asset.logged_user, '@', 1)
    ).order_by(func.count(Asset.id).desc()).limit(10).all()
    
    # Idade dos equipamentos (baseado em purchase_date se disponível)
    current_year = datetime.now().year
    age_data = []
    
    # Simulação de distribuição de idade (pode ser adaptado conforme dados reais)
    age_ranges = [
        ('< 1 ano', 0, 1),
        ('1-2 anos', 1, 2),
        ('2-3 anos', 2, 3),
        ('3-5 anos', 3, 5),
        ('> 5 anos', 5, 100)
    ]
    
    for label, min_age, max_age in age_ranges:
        # Se houver campo de data de compra, usar consulta real
        # count = Asset.query.filter(...).count()
        # Por enquanto, usar dados simulados
        count = Asset.query.filter(Asset.id % (max_age + 1) == 0).count()
        age_data.append((label, count))
    
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
        'status': {
            'labels': [item[0] if item[0] else 'N/A' for item in status_data],
            'data': [item[1] for item in status_data]
        },
        'operating_systems': {
            'labels': [item[0] if item[0] else 'N/A' for item in os_data],
            'data': [item[1] for item in os_data]
        },
        'manufacturers': {
            'labels': [item[0] if item[0] else 'N/A' for item in manufacturer_data],
            'data': [item[1] for item in manufacturer_data]
        },
        'models': {
            'labels': [item[0] if item[0] else 'N/A' for item in model_data],
            'data': [item[1] for item in model_data]
        },
        'departments': {
            'labels': [item[0] if item[0] else 'N/A' for item in department_data],
            'data': [item[1] for item in department_data]
        },
        'age_distribution': {
            'labels': [item[0] for item in age_data],
            'data': [item[1] for item in age_data]
        },
        'pmoc_manufacturers': {
            'labels': [item[0] if item[0] else 'N/A' for item in pmoc_manufacturer_data],
            'data': [item[1] for item in pmoc_manufacturer_data]
        }
    }
    
    return chart_data

# Rotas para Grupos de Assets
@bp_assets.route('/assets/groups', methods=['GET', 'POST'])
def asset_groups():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'create_group':
            try:
                name = request.form.get('name')
                description = request.form.get('description')
                
                # Validar nome único
                existing_group = AssetGroup.query.filter_by(name=name).first()
                if existing_group:
                    return jsonify({'success': False, 'message': 'Já existe um grupo com este nome'})
                
                # Criar o grupo
                group = AssetGroup(name=name, description=description)
                db.session.add(group)
                db.session.flush()  # Para obter o ID do grupo
                
                # Processar assets selecionados
                selected_assets = request.form.get('selected_assets', '[]')
                if selected_assets:
                    try:
                        assets_list = json.loads(selected_assets)
                        for asset_id in assets_list:
                            # Verificar se o asset existe
                            asset = Asset.query.get(asset_id)
                            if asset:
                                item = AssetGroupItem(group_id=group.id, asset_id=asset_id)
                                db.session.add(item)
                    except json.JSONDecodeError:
                        pass
                
                db.session.commit()
                return jsonify({'success': True, 'message': 'Grupo criado com sucesso!'})
                
            except Exception as e:
                db.session.rollback()
                return jsonify({'success': False, 'message': str(e)})
    
    # GET request
    groups = AssetGroup.query.filter_by(is_active=True).all()
    return render_template('asset_groups.html', groups=groups)

@bp_assets.route('/assets/groups/<int:group_id>/details')
def asset_group_details(group_id):
    """API endpoint para detalhes de um grupo de assets"""
    group = AssetGroup.query.get_or_404(group_id)
    
    # Obter assets do grupo
    assets_in_group = db.session.query(Asset).join(
        AssetGroupItem
    ).filter(AssetGroupItem.group_id == group_id).all()
    
    group_data = {
        'id': group.id,
        'name': group.name,
        'description': group.description,
        'created_at': group.created_at.isoformat() if group.created_at else None,
        'assets': [
            {
                'id': asset.id,
                'name': asset.name,
                'asset_tag': asset.asset_tag,
                'computer_manufacturer': asset.computer_manufacturer,
                'computer_model': asset.computer_model,
                'status': asset.status,
                'logged_user': asset.logged_user
            }
            for asset in assets_in_group
        ]
    }
    
    return jsonify(group_data)

@bp_assets.route('/assets/groups/<int:group_id>/delete', methods=['POST'])
def delete_asset_group(group_id):
    """Excluir um grupo de assets"""
    try:
        group = AssetGroup.query.get_or_404(group_id)
        
        # Registrar log antes de excluir (opcional)
        group_name = group.name
        
        # Hard delete - remover completamente do banco
        # As tabelas relacionadas serão excluídas automaticamente devido ao CASCADE
        db.session.delete(group)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Grupo "{group_name}" excluído permanentemente com sucesso!'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False, 
            'message': f'Erro ao excluir grupo: {str(e)}'
        }), 500

@bp_assets.route('/assets/groups/<int:group_id>/update', methods=['POST'])
def update_asset_group(group_id):
    """Atualizar um grupo de assets"""
    group = AssetGroup.query.get_or_404(group_id)
    
    group.name = request.form.get('name', group.name)
    group.description = request.form.get('description', group.description)
    
    # Atualizar assets se fornecidos
    if 'selected_assets' in request.form:
        # Remover assets existentes
        AssetGroupItem.query.filter_by(group_id=group_id).delete()
        
        # Adicionar novos assets
        selected_assets = request.form.get('selected_assets', '[]')
        try:
            assets_list = json.loads(selected_assets)
            for asset_id in assets_list:
                asset = Asset.query.get(asset_id)
                if asset:
                    item = AssetGroupItem(group_id=group_id, asset_id=asset_id)
                    db.session.add(item)
        except json.JSONDecodeError:
            pass
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Grupo atualizado com sucesso!'})

# APIs existentes mantidas
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
        # Contar registros PMOC para este asset
        pmoc_count = 0
        try:
            from models.database import PmocAsset
            pmoc_count = PmocAsset.query.filter_by(asset_id=asset.id).count()
        except:
            pass
        
        assets_data.append({
            'id': asset.id,
            'asset_tag': asset.asset_tag,
            'name': asset.name,
            'computer_model': asset.computer_model,
            'computer_manufacturer': asset.computer_manufacturer,
            'logged_user': asset.logged_user,
            'status': asset.status,
            'pmoc_assets_count': pmoc_count
        })
    
    return jsonify({
        'success': True,
        'assets': assets_data,
        'total': len(assets_data)
    })

@bp_assets.route('/assets/api/groups')
def assets_api_groups():
    """API endpoint para buscar grupos de assets"""
    try:
        groups = AssetGroup.query.filter_by(is_active=True).all()
        
        groups_data = []
        for group in groups:
            # Contar assets no grupo
            asset_count = AssetGroupItem.query.filter_by(group_id=group.id).count()
            
            groups_data.append({
                'id': group.id,
                'name': group.name,
                'description': group.description,
                'asset_count': asset_count,
                'created_at': group.created_at.isoformat() if group.created_at else None
            })
        
        return jsonify({
            'success': True,
            'groups': groups_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e),
            'groups': []
        }), 500

@bp_assets.route('/assets/groups/<int:group_id>/assets')
def asset_group_assets(group_id):
    """API endpoint para buscar assets de um grupo específico"""
    try:
        group = AssetGroup.query.get_or_404(group_id)
        
        # Buscar todos os assets do grupo
        assets_in_group = db.session.query(Asset).join(
            AssetGroupItem
        ).filter(AssetGroupItem.group_id == group_id).all()
        
        assets_data = []
        for asset in assets_in_group:
            assets_data.append({
                'id': asset.id,
                'name': asset.name,
                'asset_tag': asset.asset_tag,
                'computer_manufacturer': asset.computer_manufacturer,
                'computer_model': asset.computer_model,
                'ip_address': asset.ip_address,
                'status': asset.status
            })
        
        return jsonify({
            'success': True,
            'group_name': group.name,
            'assets': assets_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e),
            'assets': []
        }), 500

@bp_assets.route('/assets/api/export-csv')
def assets_api_export_csv():
    """API endpoint para exportar dados de assets em CSV"""
    from flask import Response
    import csv
    import io
    
    # Buscar todos os assets
    assets = Asset.query.all()
    
    # Criar CSV em memória
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Cabeçalho
    writer.writerow(['ID', 'Asset Tag', 'Nome', 'Modelo', 'Fabricante', 'Usuário', 'Status', 'Sistema Operacional', 'IP'])
    
    # Dados
    for asset in assets:
        writer.writerow([
            asset.id,
            asset.asset_tag or 'N/A',
            asset.name or 'N/A',
            asset.computer_model or 'N/A',
            asset.computer_manufacturer or 'N/A',
            asset.logged_user or 'N/A',
            asset.status or 'N/A',
            asset.operating_system or 'N/A',
            asset.ip_address or 'N/A'
        ])
    
    # Preparar resposta
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=assets_export.csv'}
    )

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
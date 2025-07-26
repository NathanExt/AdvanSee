from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from models.database import db, Software, InstalledSoftware, Asset, SoftwareGroup, SoftwareGroupItem, SoftwareGroupAsset, SoftwareInstallationStatus
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
import json
import os
from werkzeug.utils import secure_filename

bp_software = Blueprint('software', __name__)

@bp_software.route('/software', methods=['GET', 'POST'])
def software():
    # Parâmetros de busca
    search_name = request.args.get('search_name', '')
    search_vendor = request.args.get('search_vendor', '')
    active_tab = request.args.get('tab', 'dashboard')
    
    # Query base para InstalledSoftware agrupado por software único
    software_query = db.session.query(
        InstalledSoftware.name,
        InstalledSoftware.vendor,
        InstalledSoftware.version,
        func.count(InstalledSoftware.id).label('quantity')
    ).group_by(InstalledSoftware.name, InstalledSoftware.vendor, InstalledSoftware.version)
    
    # Aplicar filtros de busca
    if search_name:
        software_query = software_query.filter(InstalledSoftware.name.ilike(f'%{search_name}%'))
    if search_vendor:
        software_query = software_query.filter(InstalledSoftware.vendor.ilike(f'%{search_vendor}%'))
    
    # Obter lista de software instalado filtrada e agrupada
    software_list = software_query.order_by(InstalledSoftware.name).all()
    
    # Estatísticas gerais
    total_software_products = Software.query.count()
    total_installed_software = InstalledSoftware.query.count()
    unique_software_names = db.session.query(InstalledSoftware.name).distinct().count()
    
    # Dados para gráficos do Dashboard
    chart_data = get_dashboard_chart_data()
    
    # Dados para aba Grupos
    software_groups = SoftwareGroup.query.all()
    
    # Dados para aba Situação
    installation_status = get_installation_status_data()
    
    return render_template('software.html', 
                         software_list=software_list,
                         total_software_products=total_software_products,
                         total_installed_software=total_installed_software,
                         unique_software_names=unique_software_names,
                         chart_data=chart_data,
                         search_name=search_name,
                         search_vendor=search_vendor,
                         active_tab=active_tab,
                         software_groups=software_groups,
                         installation_status=installation_status)

def get_dashboard_chart_data():
    """Gera dados para os gráficos do dashboard"""
    
    # Top 10 software mais instalados
    top_installed = db.session.query(
        InstalledSoftware.name,
        func.count(InstalledSoftware.id).label('count')
    ).group_by(InstalledSoftware.name).order_by(func.count(InstalledSoftware.id).desc()).limit(10).all()
    
    # Top 10 fabricantes com mais software
    top_vendors = db.session.query(
        InstalledSoftware.vendor,
        func.count(InstalledSoftware.id).label('count')
    ).filter(InstalledSoftware.vendor.isnot(None)).group_by(InstalledSoftware.vendor).order_by(func.count(InstalledSoftware.id).desc()).limit(10).all()
    
    # Distribuição de software por fabricante
    vendor_distribution = db.session.query(
        InstalledSoftware.vendor,
        func.count(InstalledSoftware.id).label('count')
    ).filter(InstalledSoftware.vendor.isnot(None)).group_by(InstalledSoftware.vendor).order_by(func.count(InstalledSoftware.id).desc()).limit(8).all()
    
    # Gráfico geral por softwares instalados - Top 20
    general_software_chart = db.session.query(
        InstalledSoftware.name,
        func.count(InstalledSoftware.id).label('count')
    ).group_by(InstalledSoftware.name).order_by(func.count(InstalledSoftware.id).desc()).limit(20).all()
    
    # Distribuição por sistema operacional
    os_distribution = db.session.query(
        Asset.operating_system,
        func.count(Asset.id).label('count')
    ).filter(Asset.operating_system.isnot(None)).group_by(Asset.operating_system).order_by(func.count(Asset.id).desc()).limit(10).all()
    
    # Software por versão
    version_distribution = db.session.query(
        InstalledSoftware.version,
        func.count(InstalledSoftware.id).label('count')
    ).filter(InstalledSoftware.version.isnot(None)).group_by(InstalledSoftware.version).order_by(func.count(InstalledSoftware.id).desc()).limit(15).all()
    
    return {
        'top_installed': {
            'labels': [item[0] for item in top_installed],
            'data': [item[1] for item in top_installed]
        },
        'top_vendors': {
            'labels': [item[0] for item in top_vendors],
            'data': [item[1] for item in top_vendors]
        },
        'vendor_distribution': {
            'labels': [item[0] if item[0] else 'N/A' for item in vendor_distribution],
            'data': [item[1] for item in vendor_distribution]
        },
        'general_software': {
            'labels': [item[0] for item in general_software_chart],
            'data': [item[1] for item in general_software_chart]
        },
        'os_distribution': {
            'labels': [item[0] if item[0] else 'N/A' for item in os_distribution],
            'data': [item[1] for item in os_distribution]
        },
        'version_distribution': {
            'labels': [item[0] if item[0] else 'N/A' for item in version_distribution],
            'data': [item[1] for item in version_distribution]
        }
    }

def get_installation_status_data():
    """Gera dados para a aba de situação de instalação"""
    
    # Status de instalação por categoria
    status_summary = db.session.query(
        SoftwareInstallationStatus.status,
        func.count(SoftwareInstallationStatus.id).label('count')
    ).group_by(SoftwareInstallationStatus.status).all()
    
    # Problemas recentes (últimos 30 dias)
    recent_problems = SoftwareInstallationStatus.query.filter(
        and_(
            SoftwareInstallationStatus.status.in_(['failed', 'blocked']),
            SoftwareInstallationStatus.created_at >= datetime.utcnow() - timedelta(days=30)
        )
    ).order_by(SoftwareInstallationStatus.created_at.desc()).limit(50).all()
    
    # Assets com mais problemas
    problematic_assets = db.session.query(
        Asset.name,
        func.count(SoftwareInstallationStatus.id).label('problem_count')
    ).join(SoftwareInstallationStatus).filter(
        SoftwareInstallationStatus.status.in_(['failed', 'blocked'])
    ).group_by(Asset.name).order_by(func.count(SoftwareInstallationStatus.id).desc()).limit(10).all()
    
    return {
        'status_summary': status_summary,
        'recent_problems': recent_problems,
        'problematic_assets': problematic_assets
    }

# Rotas para Grupos de Software
@bp_software.route('/software/groups', methods=['GET', 'POST'])
def software_groups():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'create_group':
            try:
                name = request.form.get('name')
                description = request.form.get('description')
                is_required = request.form.get('is_required') == 'true'
                
                # Validar nome único
                existing_group = SoftwareGroup.query.filter_by(name=name).first()
                if existing_group:
                    return jsonify({'success': False, 'message': 'Já existe um grupo com este nome'})
                
                # Criar o grupo
                group = SoftwareGroup(name=name, description=description, is_required=is_required)
                db.session.add(group)
                db.session.flush()  # Para obter o ID do grupo
                
                # Processar software permitido
                allowed_software = request.form.get('allowed_software', '[]')
                if allowed_software:
                    try:
                        allowed_list = json.loads(allowed_software)
                        for software in allowed_list:
                            item = SoftwareGroupItem(
                                group_id=group.id,
                                software_name=software['name'],
                                software_vendor=software.get('vendor'),
                                software_version=software.get('version'),
                                is_required=True  # Software permitido
                            )
                            db.session.add(item)
                    except json.JSONDecodeError:
                        pass
                
                # Processar software proibido
                blocked_software = request.form.get('blocked_software', '[]')
                if blocked_software:
                    try:
                        blocked_list = json.loads(blocked_software)
                        for software in blocked_list:
                            item = SoftwareGroupItem(
                                group_id=group.id,
                                software_name=software['name'],
                                software_vendor=software.get('vendor'),
                                software_version=software.get('version'),
                                is_required=False  # Software proibido
                            )
                            db.session.add(item)
                    except json.JSONDecodeError:
                        pass
                
                # Processar assets selecionados
                selected_assets = request.form.get('selected_assets', '[]')
                if selected_assets:
                    try:
                        assets_list = json.loads(selected_assets)
                        for asset_id in assets_list:
                            assignment = SoftwareGroupAsset(group_id=group.id, asset_id=asset_id)
                            db.session.add(assignment)
                    except json.JSONDecodeError:
                        pass
                
                db.session.commit()
                return jsonify({'success': True, 'message': 'Grupo criado com sucesso!'})
                
            except Exception as e:
                db.session.rollback()
                return jsonify({'success': False, 'message': str(e)})
            
        elif action == 'add_software':
            group_id = request.form.get('group_id')
            software_name = request.form.get('software_name')
            software_vendor = request.form.get('software_vendor')
            software_version = request.form.get('software_version')
            is_required = request.form.get('is_required') == 'on'
            
            item = SoftwareGroupItem(
                group_id=group_id,
                software_name=software_name,
                software_vendor=software_vendor,
                software_version=software_version,
                is_required=is_required
            )
            db.session.add(item)
            db.session.commit()
            flash('Software adicionado ao grupo com sucesso!', 'success')
            
        elif action == 'assign_asset':
            group_id = request.form.get('group_id')
            asset_id = request.form.get('asset_id')
            
            # Verificar se já existe
            existing = SoftwareGroupAsset.query.filter_by(group_id=group_id, asset_id=asset_id).first()
            if not existing:
                assignment = SoftwareGroupAsset(group_id=group_id, asset_id=asset_id)
                db.session.add(assignment)
                db.session.commit()
                flash('Asset atribuído ao grupo com sucesso!', 'success')
            else:
                flash('Asset já está atribuído a este grupo!', 'warning')
    
    groups = SoftwareGroup.query.all()
    assets = Asset.query.all()
    
    return render_template('software_groups.html', groups=groups, assets=assets)

@bp_software.route('/software/groups/<int:group_id>')
def software_group_detail(group_id):
    group = SoftwareGroup.query.get_or_404(group_id)
    return render_template('software_group_detail.html', group=group)

@bp_software.route('/software/groups/<int:group_id>/details')
def software_group_details(group_id):
    group = SoftwareGroup.query.get_or_404(group_id)
    
    # Contar software permitido e proibido
    allowed_count = SoftwareGroupItem.query.filter_by(group_id=group_id, is_required=True).count()
    blocked_count = SoftwareGroupItem.query.filter_by(group_id=group_id, is_required=False).count()
    assets_count = SoftwareGroupAsset.query.filter_by(group_id=group_id).count()
    
    # Obter lista de software
    software_items = SoftwareGroupItem.query.filter_by(group_id=group_id).all()
    
    group_data = {
        'id': group.id,
        'name': group.name,
        'description': group.description,
        'is_required': group.is_required,
        'created_at': group.created_at.isoformat() if group.created_at else None,
        'allowed_count': allowed_count,
        'blocked_count': blocked_count,
        'assets_count': assets_count,
        'software': [
            {
                'software_name': item.software_name,
                'software_vendor': item.software_vendor,
                'software_version': item.software_version,
                'is_required': item.is_required
            }
            for item in software_items
        ]
    }
    
    return jsonify(group_data)

@bp_software.route('/software/groups/<int:group_id>/delete', methods=['POST'])
def delete_software_group(group_id):
    try:
        group = SoftwareGroup.query.get_or_404(group_id)
        
        # Deletar itens relacionados primeiro
        SoftwareGroupItem.query.filter_by(group_id=group_id).delete()
        SoftwareGroupAsset.query.filter_by(group_id=group_id).delete()
        
        # Deletar o grupo
        db.session.delete(group)
        db.session.commit()
        
        flash('Grupo de software excluído com sucesso!', 'success')
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp_software.route('/software/groups/<int:group_id>/update', methods=['POST'])
def update_software_group(group_id):
    group = SoftwareGroup.query.get_or_404(group_id)
    
    group.name = request.form.get('name')
    group.description = request.form.get('description')
    group.is_required = request.form.get('is_required') == 'on'
    
    db.session.commit()
    flash('Grupo de software atualizado com sucesso!', 'success')
    return redirect(url_for('software.software', tab='grupos'))

# Rotas para Situação de Instalação
@bp_software.route('/software/installation-status')
def installation_status():
    status_filter = request.args.get('status', '')
    asset_filter = request.args.get('asset', '')
    
    query = SoftwareInstallationStatus.query
    
    if status_filter:
        query = query.filter(SoftwareInstallationStatus.status == status_filter)
    if asset_filter:
        query = query.join(Asset).filter(Asset.name.ilike(f'%{asset_filter}%'))
    
    installation_status = query.order_by(SoftwareInstallationStatus.created_at.desc()).all()
    
    return render_template('installation_status.html', installation_status=installation_status)

@bp_software.route('/software/installation-status/<int:status_id>/update', methods=['POST'])
def update_installation_status(status_id):
    status_record = SoftwareInstallationStatus.query.get_or_404(status_id)
    
    new_status = request.form.get('status')
    blocked_reason = request.form.get('blocked_reason', '')
    
    status_record.status = new_status
    if new_status == 'blocked':
        status_record.blocked_reason = blocked_reason
    elif new_status == 'completed':
        status_record.completed_at = datetime.utcnow()
    
    db.session.commit()
    flash('Status de instalação atualizado com sucesso!', 'success')
    
    return redirect(url_for('software.installation_status'))

# APIs para AJAX
@bp_software.route('/software/api/search')
def software_api_search():
    """API endpoint para busca de software via AJAX"""
    search_name = request.args.get('search_name', '')
    search_vendor = request.args.get('search_vendor', '')
    
    software_query = db.session.query(
        InstalledSoftware.name,
        InstalledSoftware.vendor,
        InstalledSoftware.version,
        func.count(InstalledSoftware.id).label('quantity')
    ).group_by(InstalledSoftware.name, InstalledSoftware.vendor, InstalledSoftware.version)
    
    if search_name:
        software_query = software_query.filter(InstalledSoftware.name.ilike(f'%{search_name}%'))
    if search_vendor:
        software_query = software_query.filter(InstalledSoftware.vendor.ilike(f'%{search_vendor}%'))
    
    software_list = software_query.order_by(InstalledSoftware.name).limit(100).all()
    
    software_data = []
    for software in software_list:
        software_data.append({
            'name': software.name,
            'vendor': software.vendor or 'N/A',
            'version': software.version or 'N/A',
            'quantity': software.quantity
        })
    
    return jsonify(software_data)

@bp_software.route('/software/api/assets')
def software_api_assets():
    """API endpoint para buscar assets disponíveis"""
    search = request.args.get('search', '')
    
    query = Asset.query
    if search:
        query = query.filter(or_(
            Asset.name.ilike(f'%{search}%'),
            Asset.asset_tag.ilike(f'%{search}%'),
            Asset.ip_address.ilike(f'%{search}%')
        ))
    
    assets = query.limit(50).all()
    
    assets_data = []
    for asset in assets:
        assets_data.append({
            'id': asset.id,
            'name': asset.name,
            'asset_tag': asset.asset_tag,
            'ip_address': asset.ip_address or 'N/A',
            'operating_system': asset.operating_system or 'N/A'
        })
    
    return jsonify(assets_data)

@bp_software.route('/software/api/groups')
def software_api_groups():
    """API endpoint para buscar grupos de software"""
    groups = SoftwareGroup.query.all()
    
    groups_data = []
    for group in groups:
        groups_data.append({
            'id': group.id,
            'name': group.name,
            'description': group.description,
            'is_required': group.is_required,
            'software_count': len(group.group_software),
            'assets_count': len(group.group_assets)
        })
    
    return jsonify(groups_data)

@bp_software.route('/software/api/details')
def software_api_details():
    """API endpoint para detalhes de software específico"""
    name = request.args.get('name', '')
    vendor = request.args.get('vendor', '')
    version = request.args.get('version', '')
    
    # Buscar software instalado com esses parâmetros
    software_query = InstalledSoftware.query.filter(
        InstalledSoftware.name == name
    )
    
    if vendor and vendor != 'N/A':
        software_query = software_query.filter(InstalledSoftware.vendor == vendor)
    if version and version != 'N/A':
        software_query = software_query.filter(InstalledSoftware.version == version)
    
    installations = software_query.all()
    
    # Buscar assets onde este software está instalado
    assets_with_software = db.session.query(Asset).join(InstalledSoftware).filter(
        InstalledSoftware.name == name
    ).all()
    
    software_details = {
        'name': name,
        'vendor': vendor,
        'version': version,
        'total_installations': len(installations),
        'assets_with_software': [
            {
                'id': asset.id,
                'name': asset.name,
                'asset_tag': asset.asset_tag,
                'ip_address': asset.ip_address,
                'operating_system': asset.operating_system
            }
            for asset in assets_with_software
        ]
    }
    
    return jsonify(software_details)

@bp_software.route('/software/api/export-csv')
def software_api_export_csv():
    """API endpoint para exportar dados de software em CSV"""
    from flask import Response
    import csv
    import io
    
    # Buscar todos os software instalados
    software_list = db.session.query(
        InstalledSoftware.name,
        InstalledSoftware.vendor,
        InstalledSoftware.version,
        Asset.name.label('asset_name'),
        Asset.asset_tag,
        Asset.ip_address,
        Asset.operating_system
    ).join(Asset).order_by(InstalledSoftware.name).all()
    
    # Criar CSV em memória
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Cabeçalho
    writer.writerow(['Nome do Software', 'Fabricante', 'Versão', 'Asset', 'Tag do Asset', 'IP', 'Sistema Operacional'])
    
    # Dados
    for software in software_list:
        writer.writerow([
            software.name,
            software.vendor or 'N/A',
            software.version or 'N/A',
            software.asset_name,
            software.asset_tag,
            software.ip_address or 'N/A',
            software.operating_system or 'N/A'
        ])
    
    # Preparar resposta
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=software_export.csv'}
    )
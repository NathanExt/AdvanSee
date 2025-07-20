from flask import Blueprint, render_template, request, jsonify
from models.database import db, Software, InstalledSoftware
from sqlalchemy import func

bp_software = Blueprint('software', __name__)

@bp_software.route('/software')
def software():
    # Parâmetros de busca
    search_name = request.args.get('search_name', '')
    search_vendor = request.args.get('search_vendor', '')
    
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
    
    # Estatísticas gerais (todas baseadas em installed_software)
    total_software_products = Software.query.count()  # Mantém produtos cadastrados
    total_installed_software = InstalledSoftware.query.count()
    unique_software_names = db.session.query(InstalledSoftware.name).distinct().count()
    
    # Dados para gráficos
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
    
    # Distribuição de software por fabricante (baseado em installed_software)
    vendor_distribution = db.session.query(
        InstalledSoftware.vendor,
        func.count(InstalledSoftware.id).label('count')
    ).filter(InstalledSoftware.vendor.isnot(None)).group_by(InstalledSoftware.vendor).order_by(func.count(InstalledSoftware.id).desc()).limit(8).all()
    
    # Gráfico geral por softwares instalados - Top 20
    general_software_chart = db.session.query(
        InstalledSoftware.name,
        func.count(InstalledSoftware.id).label('count')
    ).group_by(InstalledSoftware.name).order_by(func.count(InstalledSoftware.id).desc()).limit(20).all()
    
    # Preparar dados para gráficos em formato JSON
    chart_data = {
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
        }
    }
    
    return render_template('software.html', 
                         software_list=software_list,
                         total_software_products=total_software_products,
                         total_installed_software=total_installed_software,
                         unique_software_names=unique_software_names,
                         chart_data=chart_data,
                         search_name=search_name,
                         search_vendor=search_vendor)

@bp_software.route('/software/api/search')
def software_api_search():
    """API endpoint para busca de software via AJAX (usando installed_software agrupado)"""
    search_name = request.args.get('search_name', '')
    search_vendor = request.args.get('search_vendor', '')
    
    # Query base para InstalledSoftware agrupado
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
    
    # Converter para formato JSON
    software_data = []
    for software in software_list:
        software_data.append({
            'name': software.name,
            'vendor': software.vendor or 'N/A',
            'version': software.version or 'N/A',
            'quantity': software.quantity
        })
    
    return jsonify(software_data)


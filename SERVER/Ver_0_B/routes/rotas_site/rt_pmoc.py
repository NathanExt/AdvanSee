from flask import Blueprint, render_template, flash, redirect, url_for
from modulos.pmoc.pmoc_main import PMOC
from modulos.pmoc.pmoc_models.pmoc_database import Notebook, Desktop

bp_pmoc = Blueprint('pmoc', __name__)

@bp_pmoc.route('/pmoc')
def pmoc():
    try:
        notebooks = Notebook.query.all()
        desktops = Desktop.query.all()
        
        
        
        pmoc_assets = []
        
        # Adicionar notebooks
        for notebook in notebooks:
            pmoc_assets.append({
                'id': notebook.id,
                'model': notebook.model,
                'patrimony': notebook.patrimony,
                'tag': notebook.tag,
                'tag_uisa': notebook.tag_uisa,
                'equipment_value': notebook.equipment_value,
                'manufacturer': notebook.manufacturer,
                'rc': notebook.rc,
                'owner': notebook.owner,
                'type': notebook.type,
                'entry_note': notebook.entry_note,
                'status': notebook.status,
                'os_version': notebook.os_version,
                'processor': notebook.processor,
                'ram_memory': notebook.ram_memory,
                'created_at': notebook.created_at,
                'updated_at': notebook.updated_at,
                'asset_type': 'Notebook'
            })
        
        # Adicionar desktops
        for desktop in desktops:
            pmoc_assets.append({
                'id': desktop.id,
                'model': desktop.model,
                'patrimony': desktop.patrimony,
                'tag': desktop.tag,
                'tag_uisa': desktop.tag_uisa,
                'equipment_value': desktop.equipment_value,
                'manufacturer': desktop.manufacturer,
                'rc': desktop.rc,
                'owner': desktop.owner,
                'type': desktop.type,
                'entry_note': desktop.entry_note,
                'status': desktop.status,
                'os_version': desktop.os_version,
                'processor': desktop.processor,
                'ram_memory': desktop.ram_memory,
                'created_at': desktop.created_at,
                'updated_at': desktop.updated_at,
                'asset_type': 'Desktop'
            })
        
        # Ordenar por ID
        pmoc_assets.sort(key=lambda x: x['id'])
        
        return render_template('pmoc.html', pmoc_assets=pmoc_assets, 
                             notebook_count=len(notebooks), 
                             desktop_count=len(desktops),
                             total_count=len(pmoc_assets))
                             
    except Exception as e:
        flash(f'Erro ao carregar dados PMOC: {str(e)}', 'error')
        return render_template('pmoc.html', pmoc_assets=[], 
                             notebook_count=0, 
                             desktop_count=0,
                             total_count=0)


@bp_pmoc.route('/pmoc_atualiza', methods=['GET'])
def pmoc_atualiza():
    try:
        pmoc = PMOC()
        pmoc.main_pmoc()
        flash('Dados PMOC atualizados com sucesso!', 'success')
        return redirect(url_for('pmoc.pmoc'))
    except Exception as e:
        flash(f'Erro ao atualizar dados PMOC: {str(e)}', 'error')
        return redirect(url_for('pmoc.pmoc'))


@bp_pmoc.route('/pmoc/notebooks')
def pmoc_notebooks():
    try:
        notebooks = Notebook.query.all()
        return render_template('pmoc_notebooks.html', notebooks=notebooks)
    except Exception as e:
        flash(f'Erro ao carregar notebooks: {str(e)}', 'error')
        return render_template('pmoc_notebooks.html', notebooks=[])


@bp_pmoc.route('/pmoc/desktops')
def pmoc_desktops():
    try:
        desktops = Desktop.query.all()
        return render_template('pmoc_desktops.html', desktops=desktops)
    except Exception as e:
        flash(f'Erro ao carregar desktops: {str(e)}', 'error')
        return render_template('pmoc_desktops.html', desktops=[])
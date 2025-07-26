"""
Rotas para Gerenciamento de Grupos de Software
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, session
from models.database import db, SoftwareGroup, SoftwareGroupItem, SoftwareGroupAsset, \
                           SoftwarePolicy, SoftwareInstallationStatus, SoftwareExecutionLog, \
                           Asset, User
from modulos.software_management.software_manager import SoftwareManager
import json
from datetime import datetime

bp_software_groups = Blueprint('software_groups', __name__)
software_manager = SoftwareManager()

@bp_software_groups.route('/software-groups')
def software_groups_list():
    """Lista todos os grupos de software"""
    try:
        groups = SoftwareGroup.query.all()
        return render_template('software_groups/list.html', groups=groups)
    except Exception as e:
        flash(f'Erro ao carregar grupos de software: {str(e)}', 'error')
        return redirect(url_for('index'))

@bp_software_groups.route('/software-groups/create', methods=['GET', 'POST'])
def create_software_group():
    """Cria um novo grupo de software"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            # Criar grupo
            group = SoftwareGroup(
                name=data['name'],
                description=data.get('description', ''),
                is_required=data.get('is_required', True)
            )
            db.session.add(group)
            db.session.commit()
            
            # Adicionar itens de software se fornecidos
            if 'software_items' in data:
                for item_data in data['software_items']:
                    item = SoftwareGroupItem(
                        group_id=group.id,
                        software_name=item_data['name'],
                        software_vendor=item_data.get('vendor'),
                        software_version=item_data.get('version'),
                        is_required=item_data.get('is_required', True)
                    )
                    db.session.add(item)
            
            # Adicionar políticas se fornecidas
            if 'policies' in data:
                for policy_data in data['policies']:
                    policy = SoftwarePolicy(
                        group_id=group.id,
                        policy_name=policy_data['name'],
                        policy_type=policy_data['type'],
                        policy_value=json.dumps(policy_data.get('value', {})),
                        is_enabled=policy_data.get('is_enabled', True)
                    )
                    db.session.add(policy)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Grupo de software criado com sucesso!',
                'group_id': group.id
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Erro ao criar grupo de software: {str(e)}'
            }), 500
    
    return render_template('software_groups/create.html')

@bp_software_groups.route('/software-groups/<int:group_id>')
def software_group_detail(group_id):
    """Exibe detalhes de um grupo de software"""
    try:
        group = SoftwareGroup.query.get_or_404(group_id)
        assets = Asset.query.all()
        return render_template('software_groups/detail.html', group=group, assets=assets)
    except Exception as e:
        flash(f'Erro ao carregar grupo de software: {str(e)}', 'error')
        return redirect(url_for('software_groups.software_groups_list'))

@bp_software_groups.route('/software-groups/<int:group_id>/edit', methods=['GET', 'POST'])
def edit_software_group(group_id):
    """Edita um grupo de software"""
    group = SoftwareGroup.query.get_or_404(group_id)
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            # Atualizar dados básicos
            group.name = data['name']
            group.description = data.get('description', '')
            group.is_required = data.get('is_required', True)
            group.updated_at = datetime.utcnow()
            
            # Atualizar itens de software
            if 'software_items' in data:
                # Remover itens existentes
                SoftwareGroupItem.query.filter_by(group_id=group.id).delete()
                
                # Adicionar novos itens
                for item_data in data['software_items']:
                    item = SoftwareGroupItem(
                        group_id=group.id,
                        software_name=item_data['name'],
                        software_vendor=item_data.get('vendor'),
                        software_version=item_data.get('version'),
                        is_required=item_data.get('is_required', True)
                    )
                    db.session.add(item)
            
            # Atualizar políticas
            if 'policies' in data:
                # Remover políticas existentes
                SoftwarePolicy.query.filter_by(group_id=group.id).delete()
                
                # Adicionar novas políticas
                for policy_data in data['policies']:
                    policy = SoftwarePolicy(
                        group_id=group.id,
                        policy_name=policy_data['name'],
                        policy_type=policy_data['type'],
                        policy_value=json.dumps(policy_data.get('value', {})),
                        is_enabled=policy_data.get('is_enabled', True)
                    )
                    db.session.add(policy)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Grupo de software atualizado com sucesso!'
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Erro ao atualizar grupo de software: {str(e)}'
            }), 500
    
    return render_template('software_groups/edit.html', group=group)

@bp_software_groups.route('/software-groups/<int:group_id>/delete', methods=['POST'])
def delete_software_group(group_id):
    """Exclui um grupo de software"""
    try:
        group = SoftwareGroup.query.get_or_404(group_id)
        db.session.delete(group)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Grupo de software excluído com sucesso!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro ao excluir grupo de software: {str(e)}'
        }), 500

@bp_software_groups.route('/software-groups/<int:group_id>/assign-assets', methods=['POST'])
def assign_assets_to_group(group_id):
    """Atribui assets a um grupo de software"""
    try:
        data = request.get_json()
        asset_ids = data.get('asset_ids', [])
        
        # Remover atribuições existentes
        SoftwareGroupAsset.query.filter_by(group_id=group_id).delete()
        
        # Adicionar novas atribuições
        for asset_id in asset_ids:
            asset_group = SoftwareGroupAsset(
                group_id=group_id,
                asset_id=asset_id,
                assigned_by=session.get('user_id', 1)  # ID do usuário logado
            )
            db.session.add(asset_group)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{len(asset_ids)} assets atribuídos ao grupo com sucesso!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro ao atribuir assets: {str(e)}'
        }), 500

@bp_software_groups.route('/assets/<int:asset_id>/software-compliance')
def asset_software_compliance(asset_id):
    """Analisa conformidade de software de um asset"""
    try:
        asset = Asset.query.get_or_404(asset_id)
        compliance_report = software_manager.analyze_software_compliance(asset_id)
        
        return render_template('software_groups/compliance.html', 
                             asset=asset, 
                             compliance=compliance_report)
    except Exception as e:
        flash(f'Erro ao analisar conformidade: {str(e)}', 'error')
        return redirect(url_for('assets.asset_detail', asset_id=asset_id))

@bp_software_groups.route('/assets/<int:asset_id>/software-compliance/api')
def asset_software_compliance_api(asset_id):
    """API para análise de conformidade de software"""
    try:
        compliance_report = software_manager.analyze_software_compliance(asset_id)
        return jsonify(compliance_report)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp_software_groups.route('/assets/<int:asset_id>/schedule-software-installation', methods=['POST'])
def schedule_software_installation(asset_id):
    """Agenda instalação/desinstalação de software"""
    try:
        data = request.get_json()
        software_list = data.get('software_list', [])
        action_type = data.get('action_type', 'install')
        scheduled_date = data.get('scheduled_date')
        
        if scheduled_date:
            scheduled_date = datetime.fromisoformat(scheduled_date.replace('Z', '+00:00'))
        
        success = software_manager.schedule_software_installation(
            asset_id, software_list, action_type, scheduled_date
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Instalação de {len(software_list)} software(s) agendada com sucesso!'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Erro ao agendar instalação'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao agendar instalação: {str(e)}'
        }), 500

@bp_software_groups.route('/assets/<int:asset_id>/execute-software-tasks', methods=['POST'])
def execute_software_tasks(asset_id):
    """Executa tarefas pendentes de software"""
    try:
        results = software_manager.execute_pending_software_tasks(asset_id)
        
        if results.get('success') is False:
            return jsonify(results), 500
        
        return jsonify({
            'success': True,
            'message': f'Executadas {results["total_tasks"]} tarefas: {results["completed"]} completadas, {results["failed"]} falharam, {results["blocked"]} bloqueadas',
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao executar tarefas: {str(e)}'
        }), 500

@bp_software_groups.route('/assets/<int:asset_id>/software-installation-status')
def software_installation_status(asset_id):
    """Obtém status de instalação de software"""
    try:
        status_list = software_manager.get_software_installation_status(asset_id)
        return jsonify({
            'success': True,
            'status_list': status_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao obter status: {str(e)}'
        }), 500

@bp_software_groups.route('/software-groups/<int:group_id>/required-software')
def get_required_software(group_id):
    """Obtém software necessário para um grupo"""
    try:
        group = SoftwareGroup.query.get_or_404(group_id)
        software_list = [
            {
                'name': item.software_name,
                'vendor': item.software_vendor,
                'version': item.software_version,
                'is_required': item.is_required
            }
            for item in group.group_software
        ]
        
        return jsonify({
            'success': True,
            'software_list': software_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao obter software: {str(e)}'
        }), 500

@bp_software_groups.route('/assets/<int:asset_id>/required-software')
def get_asset_required_software(asset_id):
    """Obtém software necessário para um asset"""
    try:
        required_software = software_manager.get_required_software_for_asset(asset_id)
        installed_software = software_manager.get_installed_software_for_asset(asset_id)
        
        return jsonify({
            'success': True,
            'required_software': required_software,
            'installed_software': installed_software
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao obter software: {str(e)}'
        }), 500

@bp_software_groups.route('/software-groups/<int:group_id>/policies')
def get_group_policies(group_id):
    """Obtém políticas de um grupo"""
    try:
        policies = SoftwarePolicy.query.filter_by(group_id=group_id).all()
        policies_list = [
            {
                'id': policy.id,
                'name': policy.policy_name,
                'type': policy.policy_type,
                'value': json.loads(policy.policy_value) if policy.policy_value else {},
                'is_enabled': policy.is_enabled
            }
            for policy in policies
        ]
        
        return jsonify({
            'success': True,
            'policies': policies_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao obter políticas: {str(e)}'
        }), 500

@bp_software_groups.route('/software-execution-logs')
def software_execution_logs():
    """Lista logs de execução de software"""
    try:
        logs = SoftwareExecutionLog.query.order_by(SoftwareExecutionLog.executed_at.desc()).limit(100).all()
        return render_template('software_groups/execution_logs.html', logs=logs)
    except Exception as e:
        flash(f'Erro ao carregar logs: {str(e)}', 'error')
        return redirect(url_for('index'))

@bp_software_groups.route('/software-execution-logs/api')
def software_execution_logs_api():
    """API para logs de execução de software"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        logs = SoftwareExecutionLog.query.order_by(
            SoftwareExecutionLog.executed_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        logs_list = [
            {
                'id': log.id,
                'asset_id': log.asset_id,
                'software_name': log.software_name,
                'action_type': log.action_type,
                'execution_status': log.execution_status,
                'execution_message': log.execution_message,
                'executed_at': log.executed_at.isoformat(),
                'executed_by': log.executed_by
            }
            for log in logs.items
        ]
        
        return jsonify({
            'success': True,
            'logs': logs_list,
            'total': logs.total,
            'pages': logs.pages,
            'current_page': logs.page
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao obter logs: {str(e)}'
        }), 500 
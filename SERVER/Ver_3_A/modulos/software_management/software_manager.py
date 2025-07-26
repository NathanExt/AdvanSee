"""
Gerenciador de Software
Responsável por gerenciar instalação, desinstalação e controle de software baseado em políticas de grupo
"""

import json
import logging
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from models.database import db, Asset, SoftwareGroup, SoftwareGroupItem, SoftwareGroupAsset, \
                           SoftwareInstallationStatus, SoftwarePolicy, SoftwareExecutionLog, \
                           InstalledSoftware
from .installers import WindowsSoftwareInstaller, LinuxSoftwareInstaller, MacOSSoftwareInstaller

logger = logging.getLogger(__name__)

class SoftwareManager:
    """Gerenciador principal de software"""
    
    def __init__(self):
        self.installers = {
            'windows': WindowsSoftwareInstaller(),
            'linux': LinuxSoftwareInstaller(),
            'macos': MacOSSoftwareInstaller()
        }
    
    def get_asset_software_groups(self, asset_id: int) -> List[SoftwareGroup]:
        """Obtém os grupos de software atribuídos a um asset"""
        try:
            asset_groups = SoftwareGroupAsset.query.filter_by(asset_id=asset_id).all()
            groups = []
            for asset_group in asset_groups:
                group = SoftwareGroup.query.get(asset_group.group_id)
                if group:
                    groups.append(group)
            return groups
        except Exception as e:
            logger.error(f"Erro ao obter grupos de software do asset {asset_id}: {e}")
            return []
    
    def get_required_software_for_asset(self, asset_id: int) -> List[Dict]:
        """Obtém a lista de software necessário para um asset baseado nos seus grupos"""
        try:
            groups = self.get_asset_software_groups(asset_id)
            required_software = []
            
            for group in groups:
                if group.is_required:
                    for item in group.group_software:
                        if item.is_required:
                            software_info = {
                                'name': item.software_name,
                                'vendor': item.software_vendor,
                                'version': item.software_version,
                                'group_id': group.id,
                                'group_name': group.name,
                                'is_required': item.is_required
                            }
                            required_software.append(software_info)
            
            return required_software
        except Exception as e:
            logger.error(f"Erro ao obter software necessário para asset {asset_id}: {e}")
            return []
    
    def get_installed_software_for_asset(self, asset_id: int) -> List[Dict]:
        """Obtém a lista de software instalado em um asset"""
        try:
            installed = InstalledSoftware.query.filter_by(asset_id=asset_id).all()
            return [
                {
                    'name': software.name,
                    'vendor': software.vendor,
                    'version': software.version
                }
                for software in installed
            ]
        except Exception as e:
            logger.error(f"Erro ao obter software instalado do asset {asset_id}: {e}")
            return []
    
    def analyze_software_compliance(self, asset_id: int) -> Dict:
        """Analisa a conformidade de software de um asset"""
        try:
            required_software = self.get_required_software_for_asset(asset_id)
            installed_software = self.get_installed_software_for_asset(asset_id)
            
            # Criar dicionário de software instalado para busca rápida
            installed_dict = {}
            for software in installed_software:
                key = f"{software['name']}_{software['vendor']}"
                installed_dict[key] = software
            
            compliance_report = {
                'asset_id': asset_id,
                'total_required': len(required_software),
                'total_installed': len(installed_software),
                'missing_software': [],
                'unwanted_software': [],
                'compliance_percentage': 0,
                'status': 'unknown'
            }
            
            # Verificar software faltante
            for required in required_software:
                key = f"{required['name']}_{required['vendor']}"
                if key not in installed_dict:
                    compliance_report['missing_software'].append(required)
            
            # Verificar software não desejado (implementar lógica de política)
            # Por enquanto, apenas software que não está em nenhum grupo
            
            # Calcular percentual de conformidade
            if compliance_report['total_required'] > 0:
                installed_count = compliance_report['total_required'] - len(compliance_report['missing_software'])
                compliance_report['compliance_percentage'] = (installed_count / compliance_report['total_required']) * 100
            
            # Determinar status
            if compliance_report['compliance_percentage'] == 100:
                compliance_report['status'] = 'compliant'
            elif compliance_report['compliance_percentage'] >= 80:
                compliance_report['status'] = 'mostly_compliant'
            elif compliance_report['compliance_percentage'] >= 50:
                compliance_report['status'] = 'partially_compliant'
            else:
                compliance_report['status'] = 'non_compliant'
            
            return compliance_report
            
        except Exception as e:
            logger.error(f"Erro ao analisar conformidade do asset {asset_id}: {e}")
            return {
                'asset_id': asset_id,
                'error': str(e),
                'status': 'error'
            }
    
    def schedule_software_installation(self, asset_id: int, software_list: List[Dict], 
                                     action_type: str = 'install', scheduled_date: Optional[datetime] = None) -> bool:
        """Agenda instalação/desinstalação de software"""
        try:
            for software in software_list:
                # Verificar se já existe uma tarefa pendente
                existing = SoftwareInstallationStatus.query.filter_by(
                    asset_id=asset_id,
                    software_name=software['name'],
                    software_vendor=software.get('vendor'),
                    status='pending'
                ).first()
                
                if existing:
                    # Atualizar tarefa existente
                    existing.action_type = action_type
                    existing.scheduled_date = scheduled_date or datetime.utcnow()
                    existing.updated_at = datetime.utcnow()
                else:
                    # Criar nova tarefa
                    new_task = SoftwareInstallationStatus(
                        asset_id=asset_id,
                        software_name=software['name'],
                        software_vendor=software.get('vendor'),
                        software_version=software.get('version'),
                        action_type=action_type,
                        status='pending',
                        scheduled_date=scheduled_date or datetime.utcnow()
                    )
                    db.session.add(new_task)
            
            db.session.commit()
            return True
            
        except Exception as e:
            logger.error(f"Erro ao agendar instalação para asset {asset_id}: {e}")
            db.session.rollback()
            return False
    
    def execute_pending_software_tasks(self, asset_id: int) -> Dict:
        """Executa tarefas pendentes de software para um asset"""
        try:
            asset = Asset.query.get(asset_id)
            if not asset:
                return {'success': False, 'error': 'Asset não encontrado'}
            
            # Determinar o sistema operacional
            os_type = self._detect_os_type(asset.operating_system)
            installer = self.installers.get(os_type)
            
            if not installer:
                return {'success': False, 'error': f'Sistema operacional não suportado: {os_type}'}
            
            # Obter tarefas pendentes
            pending_tasks = SoftwareInstallationStatus.query.filter_by(
                asset_id=asset_id,
                status='pending'
            ).all()
            
            results = {
                'asset_id': asset_id,
                'total_tasks': len(pending_tasks),
                'completed': 0,
                'failed': 0,
                'blocked': 0,
                'results': []
            }
            
            for task in pending_tasks:
                # Verificar políticas antes de executar
                if self._check_policies(asset_id, task):
                    # Marcar como em progresso
                    task.status = 'in_progress'
                    task.started_at = datetime.utcnow()
                    db.session.commit()
                    
                    # Executar a tarefa
                    result = installer.execute_software_action(
                        asset, task.software_name, task.action_type, task.software_version
                    )
                    
                    # Atualizar status da tarefa
                    if result['success']:
                        task.status = 'completed'
                        task.completed_at = datetime.utcnow()
                        results['completed'] += 1
                    else:
                        task.status = 'failed'
                        task.error_message = result.get('error', 'Erro desconhecido')
                        results['failed'] += 1
                    
                    # Registrar log de execução
                    self._log_execution(asset_id, task.software_name, task.action_type, result)
                    
                else:
                    task.status = 'blocked'
                    task.blocked_reason = 'Bloqueado por política'
                    results['blocked'] += 1
                
                results['results'].append({
                    'software_name': task.software_name,
                    'action_type': task.action_type,
                    'status': task.status,
                    'error': task.error_message
                })
                
                task.updated_at = datetime.utcnow()
            
            db.session.commit()
            return results
            
        except Exception as e:
            logger.error(f"Erro ao executar tarefas de software para asset {asset_id}: {e}")
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def _detect_os_type(self, operating_system: str) -> str:
        """Detecta o tipo de sistema operacional"""
        if not operating_system:
            return 'unknown'
        
        os_lower = operating_system.lower()
        if 'windows' in os_lower:
            return 'windows'
        elif 'linux' in os_lower:
            return 'linux'
        elif 'mac' in os_lower or 'darwin' in os_lower:
            return 'macos'
        else:
            return 'unknown'
    
    def _check_policies(self, asset_id: int, task: SoftwareInstallationStatus) -> bool:
        """Verifica políticas antes de executar uma tarefa"""
        try:
            # Obter grupos do asset
            asset_groups = SoftwareGroupAsset.query.filter_by(asset_id=asset_id).all()
            
            for asset_group in asset_groups:
                # Verificar políticas do grupo
                policies = SoftwarePolicy.query.filter_by(
                    group_id=asset_group.group_id,
                    is_enabled=True
                ).all()
                
                for policy in policies:
                    if not self._evaluate_policy(policy, task):
                        return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao verificar políticas para asset {asset_id}: {e}")
            return False
    
    def _evaluate_policy(self, policy: SoftwarePolicy, task: SoftwareInstallationStatus) -> bool:
        """Avalia uma política específica"""
        try:
            if policy.policy_type == 'blocking':
                policy_data = json.loads(policy.policy_value)
                if policy_data.get('prevent_uninstall') and task.action_type == 'uninstall':
                    return False
                if policy_data.get('prevent_install') and task.action_type == 'install':
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao avaliar política {policy.policy_name}: {e}")
            return True  # Em caso de erro, permitir a execução
    
    def _log_execution(self, asset_id: int, software_name: str, action_type: str, result: Dict):
        """Registra log de execução"""
        try:
            log = SoftwareExecutionLog(
                asset_id=asset_id,
                software_name=software_name,
                action_type=action_type,
                execution_status='success' if result['success'] else 'failed',
                execution_message=result.get('message', ''),
                execution_details=result
            )
            db.session.add(log)
            db.session.commit()
            
        except Exception as e:
            logger.error(f"Erro ao registrar log de execução: {e}")
            db.session.rollback()
    
    def get_software_installation_status(self, asset_id: int) -> List[Dict]:
        """Obtém o status de instalação de software de um asset"""
        try:
            status_list = SoftwareInstallationStatus.query.filter_by(asset_id=asset_id).all()
            return [
                {
                    'id': status.id,
                    'software_name': status.software_name,
                    'software_vendor': status.software_vendor,
                    'software_version': status.software_version,
                    'action_type': status.action_type,
                    'status': status.status,
                    'error_message': status.error_message,
                    'blocked_reason': status.blocked_reason,
                    'scheduled_date': status.scheduled_date.isoformat() if status.scheduled_date else None,
                    'started_at': status.started_at.isoformat() if status.started_at else None,
                    'completed_at': status.completed_at.isoformat() if status.completed_at else None,
                    'created_at': status.created_at.isoformat()
                }
                for status in status_list
            ]
        except Exception as e:
            logger.error(f"Erro ao obter status de instalação do asset {asset_id}: {e}")
            return [] 
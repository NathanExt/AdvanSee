




from flask import Blueprint, render_template, flash, redirect, request, url_for
from models.database import db, Asset, AssetSoftware, AssetVulnerability, AssetPatch, Agent, AssetHistory, InstalledSoftware, NetworkInterface, WindowsUpdate, PmocAsset # Importar novos modelos
from comand.comands import COMANDOS # Supondo que 'comand' é um módulo no seu projeto
from modulos.pmoc.pmoc_search import search_pmoc_asset
from modulos.ad_users.ad_search import search_ad_user
import os
bp_asset_detail = Blueprint('asset_detail', __name__)

def dados_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)

    # Busca de software original (se ainda for usada para licenças, etc.)
    asset_software = AssetSoftware.query.filter_by(asset_id=asset.id).options(db.joinedload(AssetSoftware.software)).all()
    
    # Novos dados
    installed_software_entries = InstalledSoftware.query.filter_by(asset_id=asset.id).all()
    network_interfaces = NetworkInterface.query.filter_by(asset_id=asset.id).all()
    windows_updates = WindowsUpdate.query.filter_by(asset_id=asset.id).all() # Correção aqui para o novo nome da tabela

    asset_vulnerabilities = AssetVulnerability.query.filter_by(asset_id=asset.id).options(db.joinedload(AssetVulnerability.vulnerability)).all()
    asset_patches = AssetPatch.query.filter_by(asset_id=asset.id).options(db.joinedload(AssetPatch.patch)).all()
    asset_history = AssetHistory.query.filter_by(asset_id=asset.id).order_by(AssetHistory.timestamp.desc()).all()
    
    
    agent = Agent.query.filter_by(asset_id=asset.id).first()

    # Extrair dados do JSONB de agent.configuration se o agente existir
    running_processes = []
    windows_services = []
    if agent and agent.configuration:
        running_processes = agent.configuration.get('running_processes', [])
        windows_services = agent.configuration.get('windows_services', [])

    # Buscar informações no PMOC
    pmoc_info = None
    try:
        # Usa o nome do asset como hostname ou fallback para asset_tag
        hostname = asset.name if asset.name else asset.asset_tag
        tag = asset.tag if asset.tag else None
        
        if hostname or tag:
            pmoc_results = search_pmoc_asset(hostname, tag)
            if pmoc_results and 'error' not in pmoc_results and pmoc_results.get('total_found', 0) > 0:
                pmoc_info = pmoc_results
    except Exception as e:
        print(f"Erro ao buscar informações PMOC para asset {asset_id}: {e}")
        pmoc_info = None

    return (
        asset, 
        asset_software, # Manter para compatibilidade se AssetSoftware ainda for usado
        installed_software_entries, 
        network_interfaces, 
        windows_updates,
        asset_vulnerabilities, 
        asset_patches, 
        asset_history, 
        agent,
        running_processes,
        windows_services,
        pmoc_info
    )

def dados_user(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    print(asset.logged_user.split('>')[1])
    user_data = search_ad_user(asset.logged_user.split('>')[1])
    
    if user_data:
        print(user_data['display_name'])
        return user_data
    else:
        print("Usuário não encontrado no AD")
        return None




@bp_asset_detail.route('/asset/<int:asset_id>')
def asset_detail(asset_id):
    # Desempacotar todas as variáveis retornadas por dados_asset
    ad_user = dados_user(asset_id)
    (asset,
     asset_software, 
     installed_software_entries, 
     network_interfaces, 
     windows_updates,
     asset_vulnerabilities, 
     asset_patches, 
     asset_history, 
     agent,
     running_processes,
     windows_services,
     pmoc_info) = dados_asset(asset_id)

    
    return render_template('asset_detail.html',
                           asset=asset,
                           asset_software=asset_software, # Manter para compatibilidade
                           installed_software_entries=installed_software_entries, # Nova variável
                           network_interfaces=network_interfaces, # Nova variável
                           windows_updates=windows_updates, # Nova variável
                           asset_vulnerabilities=asset_vulnerabilities,
                           asset_patches=asset_patches,
                           asset_history=asset_history,
                           agent=agent,
                           running_processes=running_processes, # Nova variável
                           windows_services=windows_services, # Nova variável
                           pmoc_info=pmoc_info, # Nova variável
                           ad_user = ad_user
                           )

@bp_asset_detail.route('/send_command/<int:asset_id>/<command_type>', methods=['POST'])
def send_command(asset_id, command_type):
    # Desempacotar todas as variáveis
    (asset,
     asset_software,
     installed_software_entries,
     network_interfaces,
     windows_updates,
     asset_vulnerabilities,
     asset_patches,
     asset_history,
     agent,
     running_processes,
     windows_services,
     pmoc_info) = dados_asset(asset_id)

    allowed_commands = ['PROCESSOS', 'FORCE_GPO', 'FORCE_CHECKIN']
    resposta = "Comando não reconhecido ou enviado."

    if command_type not in allowed_commands:
        flash('Comando inválido.', 'danger')
    else:
        if asset.ip_address:
            # O agente espera um JSON com a chave 'command'
            command_payload = {'command': command_type} 
            resposta_comando = COMANDOS.send_command_to_agent(command_payload, asset.ip_address)
            flash(f'Comando "{command_type}" enviado para o ativo {asset.name}. Resposta do agente: {resposta_comando}', 'info')
            resposta = resposta_comando
        else:
            flash(f'Ativo {asset.name} não possui endereço IP para enviar comando.', 'warning')
            resposta = "Ativo sem IP."

    print("command_type: ", command_type)
    
    return render_template('asset_detail.html',
                           asset=asset,
                           asset_software=asset_software,
                           installed_software_entries=installed_software_entries,
                           network_interfaces=network_interfaces,
                           windows_updates=windows_updates,
                           asset_vulnerabilities=asset_vulnerabilities,
                           asset_patches=asset_patches,
                           asset_history=asset_history,
                           agent=agent,
                           running_processes=running_processes,
                           windows_services=windows_services,
                           pmoc_info=pmoc_info)

@bp_asset_detail.route('/asset/<int:asset_id>/install_msi', methods=['POST'])
def install_msi(asset_id):
    # Desempacotar todas as variáveis
    print("install_msi")
    print("asset_id: ", asset_id)
    exit()
    # Obter os dados do formulário
    file = request.files['file']
    if file.filename == '':
        flash('Nenhum arquivo selecionado', 'danger')
        return redirect(url_for('asset_detail.asset_detail', asset_id=asset_id))
    
    # Salvar o arquivo temporariamente
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Enviar o comando para o agente
    command_payload = {
        'command': 'DOWNLOAD_AND_INSTALL',
        'data': {
            'url': file_path,
            'filename': file.filename
        }
    }
    resposta_comando = COMANDOS.send_command_to_agent(command_payload, asset.ip_address)
    flash(f'Instalação de MSI iniciada para o ativo {asset.name}. Resposta do agente: {resposta_comando}', 'info')
    return redirect(url_for('asset_detail.asset_detail', asset_id=asset_id))

@bp_asset_detail.route('/asset/<int:asset_id>/delete', methods=['POST'])
def delete_asset(asset_id):
    """
    Exclui um asset e todos os seus vínculos do banco de dados
    """
    try:
        # Buscar o asset
        asset = Asset.query.get_or_404(asset_id)
        asset_name = asset.name
        
        # Contar registros relacionados para logging
        agent_count = Agent.query.filter_by(asset_id=asset_id).count()
        software_count = InstalledSoftware.query.filter_by(asset_id=asset_id).count()
        network_count = NetworkInterface.query.filter_by(asset_id=asset_id).count()
        windows_updates_count = WindowsUpdate.query.filter_by(asset_id=asset_id).count()
        vulnerabilities_count = AssetVulnerability.query.filter_by(asset_id=asset_id).count()
        patches_count = AssetPatch.query.filter_by(asset_id=asset_id).count()
        history_count = AssetHistory.query.filter_by(asset_id=asset_id).count()
        pmoc_count = PmocAsset.query.filter_by(asset_id=asset_id).count()
        
        # Excluir registros relacionados (cascade não funciona para todos)
        # Agente
        Agent.query.filter_by(asset_id=asset_id).delete()
        
        # Software instalado
        InstalledSoftware.query.filter_by(asset_id=asset_id).delete()
        
        # Interfaces de rede
        NetworkInterface.query.filter_by(asset_id=asset_id).delete()
        
        # Atualizações do Windows
        WindowsUpdate.query.filter_by(asset_id=asset_id).delete()
        
        # Vulnerabilidades do asset
        AssetVulnerability.query.filter_by(asset_id=asset_id).delete()
        
        # Patches do asset
        AssetPatch.query.filter_by(asset_id=asset_id).delete()
        
        # Histórico do asset
        AssetHistory.query.filter_by(asset_id=asset_id).delete()
        
        # Registros PMOC
        PmocAsset.query.filter_by(asset_id=asset_id).delete()
        
        # Software do asset (AssetSoftware)
        AssetSoftware.query.filter_by(asset_id=asset_id).delete()
        
        # Finalmente, excluir o asset
        db.session.delete(asset)
        db.session.commit()
        
        # Log da exclusão
        print(f"Asset '{asset_name}' (ID: {asset_id}) excluído com sucesso.")
        print(f"Registros excluídos:")
        print(f"  - Agente: {agent_count}")
        print(f"  - Software instalado: {software_count}")
        print(f"  - Interfaces de rede: {network_count}")
        print(f"  - Atualizações Windows: {windows_updates_count}")
        print(f"  - Vulnerabilidades: {vulnerabilities_count}")
        print(f"  - Patches: {patches_count}")
        print(f"  - Histórico: {history_count}")
        print(f"  - Registros PMOC: {pmoc_count}")
        
        flash(f'Asset "{asset_name}" excluído com sucesso! Todos os vínculos foram removidos.', 'success')
        return redirect(url_for('assets.assets'))
        
    except Exception as e:
        db.session.rollback()
        error_msg = f'Erro ao excluir asset: {str(e)}'
        print(error_msg)
        flash(error_msg, 'danger')
        return redirect(url_for('asset_detail.asset_detail', asset_id=asset_id))


@bp_asset_detail.route('/asset/<int:asset_id>/active_events', methods=['POST'])
def active_events(asset_id):
    print("HABILITAR EVENTOS")
    pass
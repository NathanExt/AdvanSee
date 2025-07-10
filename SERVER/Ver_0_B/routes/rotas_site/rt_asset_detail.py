from flask import Blueprint, render_template, flash, redirect
from models.database import db, Asset, AssetSoftware, AssetVulnerability, AssetPatch, Agent, AssetHistory, InstalledSoftware, NetworkInterface, WindowsUpdate # Importar novos modelos
from comand.comands import COMANDOS # Supondo que 'comand' é um módulo no seu projeto

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
        windows_services
    )

@bp_asset_detail.route('/asset/<int:asset_id>')
def asset_detail(asset_id):
    # Desempacotar todas as variáveis retornadas por dados_asset
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
     windows_services) = dados_asset(asset_id)

    # A variável 'resposta' não é definida aqui, remova-a se não for usada.
    # Se for para mostrar alguma mensagem após o comando, o flash é mais adequado.
    resposta = "Não Carregado" 
    
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
                           resposta=resposta)

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
     windows_services) = dados_asset(asset_id)

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
                           windows_services=windows_services)
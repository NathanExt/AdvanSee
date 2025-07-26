from flask import Blueprint, render_template, request, json, jsonify
from models.database import db, Asset, Agent, Organization, AssetHistory, InstalledSoftware, NetworkInterface, WindowsUpdate
from datetime import datetime
from config import CONFIG
from cryptography.fernet import Fernet
from modulos.pmoc.pmoc_search import search_pmoc_asset

bp_agente_checkin = Blueprint('checkin', __name__)

ENCRYPTION_KEY_BYTES = CONFIG.ENCRYPTION_KEY
CIPHER_SUITE = Fernet(ENCRYPTION_KEY_BYTES)


@bp_agente_checkin.route('/checkin', methods=['POST'])
def agent_checkin():
    try:
        data_from_agent = request.get_json()
        encrypted_payload_str = data_from_agent.get('encrypted_payload')

        if not encrypted_payload_str:
            return jsonify({'error': 'No encrypted_payload found in request'}), 400

        encrypted_data_bytes = encrypted_payload_str.encode('latin-1')
        data_decript_bytes = CIPHER_SUITE.decrypt(encrypted_data_bytes)
        data = json.loads(data_decript_bytes.decode('utf-8'))
        
        #print(data) # For server-side debugging

        asset_tag = data.get('asset_tag')
        agent_version = data.get('agent_version')
        system_info = data.get('system_info', {})
        
        if not asset_tag:
            return jsonify({'error': 'Asset tag is required'}), 400
        
        organization = Organization.query.first()
        if not organization:
            return jsonify({'error': 'No organization found to assign asset'}), 500
        organization_id = organization.id

        asset = Asset.query.filter_by(asset_tag=asset_tag, organization_id=organization_id).first()
        newly_created_asset = False
        
        if not asset:
            # Extract disk_info for direct columns in Asset
            disk_info = system_info.get('disk_info', [{}])[0] if system_info.get('disk_info') else {}
            memory_info = system_info.get('memory_info', {})

            asset = Asset(
                organization_id=organization_id,
                asset_tag=asset_tag,
                tag=system_info.get('tag'),  # Adiciona a tag do asset
                name=system_info.get('hostname', f'Asset-{asset_tag[:8]}'),
                description='Discovered by agent check-in',
                status='active',
                criticality='medium',
                ip_address=system_info.get('ip_address'),
                mac_address=system_info.get('mac_address'),
                operating_system=system_info.get('operating_system'),
                os_version=system_info.get('os_version'),
                python_version=system_info.get('python_version'),
                logged_user=system_info.get('logged_user'),
                architecture=system_info.get('architecture'),
                processor=system_info.get('processor'),
                cpu_count=system_info.get('cpu_count'),
                cpu_count_logical=system_info.get('cpu_count_logical'),
                cpu_freq_current=system_info.get('cpu_freq_current'),
                cpu_freq_min=system_info.get('cpu_freq_min'),
                cpu_freq_max=system_info.get('cpu_freq_max'),
                total_memory_bytes=memory_info.get('total_bytes'),
                available_memory_bytes=memory_info.get('available_bytes'),
                memory_percent=memory_info.get('percent'),
                total_disk_bytes=disk_info.get('total_bytes'),
                used_disk_bytes=disk_info.get('used_bytes'),
                free_disk_bytes=disk_info.get('free_bytes'),
                disk_percent=disk_info.get('percent'),
                disk_model=disk_info.get('model'),
                disk_serial=disk_info.get('serial'),
                disk_interface_type=disk_info.get('interface_type'),
                computer_model=system_info.get('computer_model'),
                computer_manufacturer=system_info.get('computer_manufacturer'),
                computer_system_type=system_info.get('computer_system_type'),
                last_seen=datetime.utcnow(),
                created_at=datetime.utcnow()
            )
            db.session.add(asset)
            db.session.flush() # To get asset.id for related tables
            newly_created_asset = True
            history = AssetHistory(
                asset_id=asset.id,
                user_id=None, 
                action='created by agent',
                new_value=f'Asset automatically created by agent with tag {asset_tag}'
            )
            db.session.add(history)

        agent = Agent.query.filter_by(asset_id=asset.id).first()
        
        if not agent:
            agent = Agent(
                asset_id=asset.id,
                agent_version=agent_version,
                status='active'
            )
            db.session.add(agent)
        else:
            agent.agent_version = agent_version
            agent.status = 'active'
        
        agent.last_checkin = datetime.utcnow()
        
        # Store comprehensive system_info, running_processes, and windows_services in agent.configuration JSONB
        agent_config_data = {
            "running_processes": system_info.get("running_processes", []),
            "windows_services": system_info.get("windows_services", []),
            # Potentially store other less-structured or less-queried info here
            # "raw_system_info": system_info # If you want to keep the whole raw data
        }
        agent.configuration = agent_config_data
        agent.updated_at = datetime.utcnow()
        
        if system_info:
            updated_fields = []

            # Update Asset direct columns from system_info
            fields_to_update = {
                'tag': system_info.get('tag'),  # Adiciona a tag do asset
                'ip_address': system_info.get('ip_address'),
                'mac_address': system_info.get('mac_address'),
                'operating_system': system_info.get('operating_system'),
                'os_version': system_info.get('os_version'),
                'python_version': system_info.get('python_version'),
                'logged_user': system_info.get('logged_user'),
                'architecture': system_info.get('architecture'),
                'processor': system_info.get('processor'),
                'cpu_count': system_info.get('cpu_count'),
                'cpu_count_logical': system_info.get('cpu_count_logical'),
                'cpu_freq_current': system_info.get('cpu_freq_current'),
                'cpu_freq_min': system_info.get('cpu_freq_min'),
                'cpu_freq_max': system_info.get('cpu_freq_max'),
                'computer_model': system_info.get('computer_model'),
                'computer_manufacturer': system_info.get('computer_manufacturer'),
                'computer_system_type': system_info.get('computer_system_type'),
            }

            memory_info = system_info.get('memory_info', {})
            fields_to_update.update({
                'total_memory_bytes': memory_info.get('total_bytes'),
                'available_memory_bytes': memory_info.get('available_bytes'),
                'memory_percent': memory_info.get('percent'),
            })

            disk_info = system_info.get('disk_info', [{}])[0] if system_info.get('disk_info') else {}
            fields_to_update.update({
                'total_disk_bytes': disk_info.get('total_bytes'),
                'used_disk_bytes': disk_info.get('used_bytes'),
                'free_disk_bytes': disk_info.get('free_bytes'),
                'disk_percent': disk_info.get('percent'),
                'disk_model': disk_info.get('model'),
                'disk_serial': disk_info.get('serial'),
                'disk_interface_type': disk_info.get('interface_type'),
            })

            for field, new_value in fields_to_update.items():
                old_value = getattr(asset, field)
                if str(old_value) != str(new_value) and new_value is not None:
                    updated_fields.append({'field': field, 'old_value': old_value, 'new_value': new_value})
                    setattr(asset, field, new_value)
            
            # Special handling for hostname as 'name'
            if 'hostname' in system_info and asset.name != system_info['hostname'] and not newly_created_asset:
                updated_fields.append({'field': 'name', 'old_value': asset.name, 'new_value': system_info['hostname']})
                asset.name = system_info['hostname']

            asset.last_seen = datetime.utcnow()
            asset.updated_at = datetime.utcnow()

            for change in updated_fields:
                history = AssetHistory(
                    asset_id=asset.id,
                    user_id=None,
                    action='updated by agent',
                    field_name=change['field'],
                    old_value=str(change['old_value']),
                    new_value=str(change['new_value'])
                )
                db.session.add(history)
            
            # Process installed_software
            if 'installed_software' in system_info:
                software_added_count = 0
                software_to_insert = []
                
                for software_data in system_info['installed_software']:
                    # Aceita tanto chaves capitalizadas quanto minúsculas para compatibilidade
                    name = software_data.get('Name') or software_data.get('name')
                    version = software_data.get('Version') or software_data.get('version')
                    vendor = software_data.get('Vendor') or software_data.get('vendor')

                    # Só processa se pelo menos o nome estiver presente
                    if name:
                        software_to_insert.append({
                            'asset_id': asset.id,
                            'name': name,
                            'version': version,
                            'vendor': vendor,
                            'created_at': datetime.utcnow()
                        })
                
                # Usa bulk insert com ON CONFLICT DO NOTHING para evitar duplicatas
                if software_to_insert:
                    try:
                        from sqlalchemy.dialects.postgresql import insert
                        stmt = insert(InstalledSoftware).values(software_to_insert)
                        stmt = stmt.on_conflict_do_nothing(
                            index_elements=['asset_id', 'name', 'version', 'vendor']
                        )
                        result = db.session.execute(stmt)
                        software_added_count = result.rowcount
                        
                        # Adiciona entrada no histórico apenas se software foi realmente adicionado
                        if software_added_count > 0:
                            history = AssetHistory(
                                asset_id=asset.id,
                                user_id=None,
                                action='installed_software_sync',
                                new_value=f'Sincronizados {software_added_count} softwares instalados'
                            )
                            db.session.add(history)
                            
                    except Exception as e:
                        print(f"Erro ao processar software instalado para asset {asset.id}: {str(e)}")
                        # Fallback para inserção individual em caso de erro
                        for software_info in software_to_insert:
                            try:
                                existing_software = InstalledSoftware.query.filter_by(
                                    asset_id=software_info['asset_id'],
                                    name=software_info['name'],
                                    version=software_info['version'],
                                    vendor=software_info['vendor']
                                ).first()
                                
                                if not existing_software:
                                    new_software = InstalledSoftware(**software_info)
                                    db.session.add(new_software)
                                    software_added_count += 1
                                    
                            except Exception as inner_e:
                                print(f"Erro ao inserir software individual: {software_info['name']} - {str(inner_e)}")
                                continue
                                
                # Log da quantidade de softwares processados
                if software_added_count > 0:
                    print(f"Adicionados {software_added_count} novos softwares para o asset {asset.id}")
                # You might want logic here to remove software no longer reported

            # Process network_interfaces
            if 'network_interfaces' in system_info:
                # Clear existing interfaces to resync, or implement a more granular update
                # For simplicity, we delete and re-add for this example
                NetworkInterface.query.filter_by(asset_id=asset.id).delete()
                
                for interface_data in system_info['network_interfaces']:
                    interface_name = interface_data.get('name')
                    for addr_data in interface_data.get('addresses', []):
                        new_interface = NetworkInterface(
                            asset_id=asset.id,
                            name=interface_name,
                            family=addr_data.get('family'),
                            ip_address=addr_data.get('address') if addr_data.get('family') in ['2', '23'] else None,
                            mac_address=addr_data.get('address') if addr_data.get('family') == '-1' else None,
                            netmask=addr_data.get('netmask'),
                            broadcast=addr_data.get('broadcast')
                        )
                        db.session.add(new_interface)
                history = AssetHistory(
                    asset_id=asset.id,
                    user_id=None,
                    action='network_interfaces_updated',
                    new_value='Network interfaces updated'
                )
                db.session.add(history)

            # Process windows_updates
            if 'windows_updates' in system_info and system_info['windows_updates'].get('updates'):
                current_updates_on_asset = {
                    wu.hotfix_id for wu in asset.windows_updates_entries
                }

                for update_data in system_info['windows_updates']['updates']:
                    hotfix_id = update_data.get('HotFixID')
                    if hotfix_id and hotfix_id not in current_updates_on_asset:
                        installed_on_date = None
                        try:
                            # Assuming "MM/DD/YYYY" format based on log_pacote.txt
                            installed_on_date = datetime.strptime(update_data.get('InstalledOn'), '%m/%d/%Y').date()
                        except (ValueError, TypeError):
                            pass # Handle cases where date is missing or malformed

                        new_update = WindowsUpdate(
                            asset_id=asset.id,
                            hotfix_id=hotfix_id,
                            description=update_data.get('Description'),
                            installed_on=installed_on_date,
                            installed_by=update_data.get('InstalledBy')
                        )
                        db.session.add(new_update)
                        history = AssetHistory(
                            asset_id=asset.id,
                            user_id=None,
                            action='windows_update_added',
                            new_value=f'Windows Update installed: {hotfix_id} ({update_data.get("Description")})'
                        )
                        db.session.add(history)
                # Add logic to remove updates that are no longer present if desired

        # Buscar informações complementares no banco PMOC
        try:
            # Extrai hostname do nome do asset ou usa o asset_tag
            hostname = asset.name if asset.name else asset.asset_tag
            tag = asset.tag if asset.tag else None
            
            if hostname or tag:
                print(f"Buscando informações no PMOC para hostname: {hostname}, tag: {tag}")
                pmoc_results = search_pmoc_asset(hostname, tag)
                
                if pmoc_results and 'error' not in pmoc_results and pmoc_results.get('total_found', 0) > 0:
                    # Adicionar informações encontradas no histórico
                    pmoc_info = []
                    
                    for notebook in pmoc_results.get('notebooks', []):
                        pmoc_info.append(f"Notebook PMOC: {notebook['id']} - {notebook['model']} - Patrimônio: {notebook['patrimony']} - Owner: {notebook['owner']}")
                    
                    for desktop in pmoc_results.get('desktops', []):
                        pmoc_info.append(f"Desktop PMOC: {desktop['id']} - {desktop['model']} - Patrimônio: {desktop['patrimony']} - Owner: {desktop['owner']}")
                    
                    if pmoc_info:
                        history = AssetHistory(
                            asset_id=asset.id,
                            user_id=None,
                            action='pmoc_info_found',
                            new_value=f"Informações PMOC encontradas: {'; '.join(pmoc_info)}"
                        )
                        db.session.add(history)
                        print(f"Informações PMOC adicionadas ao histórico do asset {asset.id}")
                    
                else:
                    print(f"Nenhuma informação encontrada no PMOC para hostname: {hostname}, tag: {tag}")
                    
        except Exception as pmoc_error:
            print(f"Erro ao buscar no PMOC: {pmoc_error}")
            # Não falha o checkin se houver erro na busca PMOC
            
        db.session.commit()
        
        response_data = {
            'message': 'Check-in successful',
            'agent_id': agent.id,
            'commands': []
        }
        
        response_json_bytes = json.dumps(response_data).encode('utf-8')
        encrypted_response_bytes = CIPHER_SUITE.encrypt(response_json_bytes)
        
        return jsonify({
            "encrypted_response": encrypted_response_bytes.decode('latin-1')
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error during agent check-in: {e}") # Log the error for debugging
        return jsonify({'error': str(e)}), 500

@bp_agente_checkin.route('/checkin', methods=['GET'])
def agent_checkin_brw():
    return render_template('checkin.html')
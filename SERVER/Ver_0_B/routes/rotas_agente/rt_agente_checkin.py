from flask import Blueprint, render_template, request, json, jsonify
from models.database import db, Asset, Agent, Organization, AssetHistory, InstalledSoftware, NetworkInterface, WindowsUpdate
from datetime import datetime
from config import Config
from cryptography.fernet import Fernet

bp_agente_checkin = Blueprint('checkin', __name__)

ENCRYPTION_KEY_BYTES = Config.ENCRYPTION_KEY
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
        
        print(data) # For server-side debugging

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
                name=system_info.get('hostname', f'Asset-{asset_tag[:8]}'),
                description='Discovered by agent check-in',
                status='active',
                criticality='medium',
                ip_address=system_info.get('ip_address'),
                mac_address=system_info.get('mac_address'),
                operating_system=system_info.get('operating_system'),
                os_version=system_info.get('os_version'),
                python_version=system_info.get('python_version'),
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
                'ip_address': system_info.get('ip_address'),
                'mac_address': system_info.get('mac_address'),
                'operating_system': system_info.get('operating_system'),
                'os_version': system_info.get('os_version'),
                'python_version': system_info.get('python_version'),
                'architecture': system_info.get('architecture'),
                'processor': system_info.get('processor'),
                'cpu_count': system_info.get('cpu_count'),
                'cpu_count_logical': system_info.get('cpu_count_logical'),
                'cpu_freq_current': system_info.get('cpu_freq_current'),
                'cpu_freq_min': system_info.get('cpu_freq_min'),
                'cpu_freq_max': system_info.get('cpu_freq_max'),
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
                current_software_on_asset = {
                    (s.name, s.version, s.vendor) for s in asset.installed_software_entries
                }
                
                for software_data in system_info['installed_software']:
                    name = software_data.get('Name')
                    version = software_data.get('Version')
                    vendor = software_data.get('Vendor')

                    if (name, version, vendor) not in current_software_on_asset:
                        new_software = InstalledSoftware(
                            asset_id=asset.id,
                            name=name,
                            version=version,
                            vendor=vendor
                        )
                        db.session.add(new_software)
                        history = AssetHistory(
                            asset_id=asset.id,
                            user_id=None,
                            action='installed_software_added',
                            new_value=f'Software installed: {name} {version} ({vendor})'
                        )
                        db.session.add(history)
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
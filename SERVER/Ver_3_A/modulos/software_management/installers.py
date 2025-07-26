"""
Instaladores de Software
Implementações específicas para diferentes sistemas operacionais
"""

import subprocess
import logging
import os
import json
from typing import Dict, Optional
from models.database import Asset

logger = logging.getLogger(__name__)

class BaseSoftwareInstaller:
    """Classe base para instaladores de software"""
    
    def __init__(self):
        self.supported_software = {}
        self.installation_methods = {}
    
    def execute_software_action(self, asset: Asset, software_name: str, action_type: str, version: Optional[str] = None) -> Dict:
        """Executa uma ação de software (instalar/desinstalar)"""
        try:
            if action_type == 'install':
                return self.install_software(asset, software_name, version)
            elif action_type == 'uninstall':
                return self.uninstall_software(asset, software_name, version)
            elif action_type == 'update':
                return self.update_software(asset, software_name, version)
            else:
                return {'success': False, 'error': f'Ação não suportada: {action_type}'}
        except Exception as e:
            logger.error(f"Erro ao executar ação de software: {e}")
            return {'success': False, 'error': str(e)}
    
    def install_software(self, asset: Asset, software_name: str, version: Optional[str] = None) -> Dict:
        """Instala software (deve ser implementado pelas subclasses)"""
        raise NotImplementedError
    
    def uninstall_software(self, asset: Asset, software_name: str, version: Optional[str] = None) -> Dict:
        """Desinstala software (deve ser implementado pelas subclasses)"""
        raise NotImplementedError
    
    def update_software(self, asset: Asset, software_name: str, version: Optional[str] = None) -> Dict:
        """Atualiza software (deve ser implementado pelas subclasses)"""
        raise NotImplementedError
    
    def check_software_installed(self, asset: Asset, software_name: str) -> bool:
        """Verifica se software está instalado (deve ser implementado pelas subclasses)"""
        raise NotImplementedError
    
    def execute_remote_command(self, asset: Asset, command: str) -> Dict:
        """Executa comando remoto no asset"""
        try:
            # Aqui você implementaria a lógica de execução remota
            # Por exemplo, usando SSH, WinRM, ou agentes instalados
            # Por enquanto, retornamos um mock
            
            # Simular execução de comando
            logger.info(f"Executando comando remoto em {asset.name}: {command}")
            
            return {
                'success': True,
                'output': f'Comando executado com sucesso: {command}',
                'exit_code': 0
            }
            
        except Exception as e:
            logger.error(f"Erro ao executar comando remoto: {e}")
            return {
                'success': False,
                'error': str(e),
                'exit_code': -1
            }


class WindowsSoftwareInstaller(BaseSoftwareInstaller):
    """Instalador de software para Windows"""
    
    def __init__(self):
        super().__init__()
        self.supported_software = {
            'Google Chrome': {
                'install_cmd': 'winget install Google.Chrome',
                'uninstall_cmd': 'winget uninstall Google.Chrome',
                'check_cmd': 'Get-WmiObject -Class Win32_Product | Where-Object {$_.Name -like "*Chrome*"}'
            },
            'Mozilla Firefox': {
                'install_cmd': 'winget install Mozilla.Firefox',
                'uninstall_cmd': 'winget uninstall Mozilla.Firefox',
                'check_cmd': 'Get-WmiObject -Class Win32_Product | Where-Object {$_.Name -like "*Firefox*"}'
            },
            '7-Zip': {
                'install_cmd': 'winget install 7zip.7zip',
                'uninstall_cmd': 'winget uninstall 7zip.7zip',
                'check_cmd': 'Get-WmiObject -Class Win32_Product | Where-Object {$_.Name -like "*7-Zip*"}'
            },
            'Adobe Reader': {
                'install_cmd': 'winget install Adobe.AdobeAcrobatReaderDC',
                'uninstall_cmd': 'winget uninstall Adobe.AdobeAcrobatReaderDC',
                'check_cmd': 'Get-WmiObject -Class Win32_Product | Where-Object {$_.Name -like "*Adobe Reader*"}'
            },
            'Visual Studio Code': {
                'install_cmd': 'winget install Microsoft.VisualStudioCode',
                'uninstall_cmd': 'winget uninstall Microsoft.VisualStudioCode',
                'check_cmd': 'Get-WmiObject -Class Win32_Product | Where-Object {$_.Name -like "*Visual Studio Code*"}'
            },
            'Git': {
                'install_cmd': 'winget install Git.Git',
                'uninstall_cmd': 'winget uninstall Git.Git',
                'check_cmd': 'Get-WmiObject -Class Win32_Product | Where-Object {$_.Name -like "*Git*"}'
            },
            'Python': {
                'install_cmd': 'winget install Python.Python.3.11',
                'uninstall_cmd': 'winget uninstall Python.Python.3.11',
                'check_cmd': 'python --version'
            },
            'Node.js': {
                'install_cmd': 'winget install OpenJS.NodeJS',
                'uninstall_cmd': 'winget uninstall OpenJS.NodeJS',
                'check_cmd': 'node --version'
            }
        }
    
    def install_software(self, asset: Asset, software_name: str, version: Optional[str] = None) -> Dict:
        """Instala software no Windows"""
        try:
            if software_name not in self.supported_software:
                return {'success': False, 'error': f'Software não suportado: {software_name}'}
            
            # Verificar se já está instalado
            if self.check_software_installed(asset, software_name):
                return {'success': True, 'message': f'{software_name} já está instalado'}
            
            # Obter comando de instalação
            install_cmd = self.supported_software[software_name]['install_cmd']
            
            # Executar instalação
            result = self.execute_remote_command(asset, install_cmd)
            
            if result['success']:
                return {
                    'success': True,
                    'message': f'{software_name} instalado com sucesso',
                    'details': result
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro ao instalar {software_name}: {result.get("error", "Erro desconhecido")}',
                    'details': result
                }
                
        except Exception as e:
            logger.error(f"Erro ao instalar {software_name} no Windows: {e}")
            return {'success': False, 'error': str(e)}
    
    def uninstall_software(self, asset: Asset, software_name: str, version: Optional[str] = None) -> Dict:
        """Desinstala software no Windows"""
        try:
            if software_name not in self.supported_software:
                return {'success': False, 'error': f'Software não suportado: {software_name}'}
            
            # Verificar se está instalado
            if not self.check_software_installed(asset, software_name):
                return {'success': True, 'message': f'{software_name} não está instalado'}
            
            # Obter comando de desinstalação
            uninstall_cmd = self.supported_software[software_name]['uninstall_cmd']
            
            # Executar desinstalação
            result = self.execute_remote_command(asset, uninstall_cmd)
            
            if result['success']:
                return {
                    'success': True,
                    'message': f'{software_name} desinstalado com sucesso',
                    'details': result
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro ao desinstalar {software_name}: {result.get("error", "Erro desconhecido")}',
                    'details': result
                }
                
        except Exception as e:
            logger.error(f"Erro ao desinstalar {software_name} no Windows: {e}")
            return {'success': False, 'error': str(e)}
    
    def update_software(self, asset: Asset, software_name: str, version: Optional[str] = None) -> Dict:
        """Atualiza software no Windows"""
        try:
            if software_name not in self.supported_software:
                return {'success': False, 'error': f'Software não suportado: {software_name}'}
            
            # Para Windows, usar winget upgrade
            upgrade_cmd = f'winget upgrade {software_name}'
            
            result = self.execute_remote_command(asset, upgrade_cmd)
            
            if result['success']:
                return {
                    'success': True,
                    'message': f'{software_name} atualizado com sucesso',
                    'details': result
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro ao atualizar {software_name}: {result.get("error", "Erro desconhecido")}',
                    'details': result
                }
                
        except Exception as e:
            logger.error(f"Erro ao atualizar {software_name} no Windows: {e}")
            return {'success': False, 'error': str(e)}
    
    def check_software_installed(self, asset: Asset, software_name: str) -> bool:
        """Verifica se software está instalado no Windows"""
        try:
            if software_name not in self.supported_software:
                return False
            
            check_cmd = self.supported_software[software_name]['check_cmd']
            result = self.execute_remote_command(asset, check_cmd)
            
            return result['success'] and result.get('exit_code', -1) == 0
            
        except Exception as e:
            logger.error(f"Erro ao verificar instalação de {software_name}: {e}")
            return False


class LinuxSoftwareInstaller(BaseSoftwareInstaller):
    """Instalador de software para Linux"""
    
    def __init__(self):
        super().__init__()
        self.supported_software = {
            'Google Chrome': {
                'install_cmd': 'sudo apt-get install -y google-chrome-stable',
                'uninstall_cmd': 'sudo apt-get remove -y google-chrome-stable',
                'check_cmd': 'which google-chrome'
            },
            'Mozilla Firefox': {
                'install_cmd': 'sudo apt-get install -y firefox',
                'uninstall_cmd': 'sudo apt-get remove -y firefox',
                'check_cmd': 'which firefox'
            },
            '7-Zip': {
                'install_cmd': 'sudo apt-get install -y p7zip-full',
                'uninstall_cmd': 'sudo apt-get remove -y p7zip-full',
                'check_cmd': 'which 7z'
            },
            'Git': {
                'install_cmd': 'sudo apt-get install -y git',
                'uninstall_cmd': 'sudo apt-get remove -y git',
                'check_cmd': 'which git'
            },
            'Python': {
                'install_cmd': 'sudo apt-get install -y python3',
                'uninstall_cmd': 'sudo apt-get remove -y python3',
                'check_cmd': 'python3 --version'
            },
            'Node.js': {
                'install_cmd': 'curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt-get install -y nodejs',
                'uninstall_cmd': 'sudo apt-get remove -y nodejs',
                'check_cmd': 'node --version'
            }
        }
    
    def install_software(self, asset: Asset, software_name: str, version: Optional[str] = None) -> Dict:
        """Instala software no Linux"""
        try:
            if software_name not in self.supported_software:
                return {'success': False, 'error': f'Software não suportado: {software_name}'}
            
            # Verificar se já está instalado
            if self.check_software_installed(asset, software_name):
                return {'success': True, 'message': f'{software_name} já está instalado'}
            
            # Obter comando de instalação
            install_cmd = self.supported_software[software_name]['install_cmd']
            
            # Executar instalação
            result = self.execute_remote_command(asset, install_cmd)
            
            if result['success']:
                return {
                    'success': True,
                    'message': f'{software_name} instalado com sucesso',
                    'details': result
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro ao instalar {software_name}: {result.get("error", "Erro desconhecido")}',
                    'details': result
                }
                
        except Exception as e:
            logger.error(f"Erro ao instalar {software_name} no Linux: {e}")
            return {'success': False, 'error': str(e)}
    
    def uninstall_software(self, asset: Asset, software_name: str, version: Optional[str] = None) -> Dict:
        """Desinstala software no Linux"""
        try:
            if software_name not in self.supported_software:
                return {'success': False, 'error': f'Software não suportado: {software_name}'}
            
            # Verificar se está instalado
            if not self.check_software_installed(asset, software_name):
                return {'success': True, 'message': f'{software_name} não está instalado'}
            
            # Obter comando de desinstalação
            uninstall_cmd = self.supported_software[software_name]['uninstall_cmd']
            
            # Executar desinstalação
            result = self.execute_remote_command(asset, uninstall_cmd)
            
            if result['success']:
                return {
                    'success': True,
                    'message': f'{software_name} desinstalado com sucesso',
                    'details': result
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro ao desinstalar {software_name}: {result.get("error", "Erro desconhecido")}',
                    'details': result
                }
                
        except Exception as e:
            logger.error(f"Erro ao desinstalar {software_name} no Linux: {e}")
            return {'success': False, 'error': str(e)}
    
    def update_software(self, asset: Asset, software_name: str, version: Optional[str] = None) -> Dict:
        """Atualiza software no Linux"""
        try:
            if software_name not in self.supported_software:
                return {'success': False, 'error': f'Software não suportado: {software_name}'}
            
            # Para Linux, usar apt-get upgrade
            update_cmd = f'sudo apt-get update && sudo apt-get upgrade -y {software_name}'
            
            result = self.execute_remote_command(asset, update_cmd)
            
            if result['success']:
                return {
                    'success': True,
                    'message': f'{software_name} atualizado com sucesso',
                    'details': result
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro ao atualizar {software_name}: {result.get("error", "Erro desconhecido")}',
                    'details': result
                }
                
        except Exception as e:
            logger.error(f"Erro ao atualizar {software_name} no Linux: {e}")
            return {'success': False, 'error': str(e)}
    
    def check_software_installed(self, asset: Asset, software_name: str) -> bool:
        """Verifica se software está instalado no Linux"""
        try:
            if software_name not in self.supported_software:
                return False
            
            check_cmd = self.supported_software[software_name]['check_cmd']
            result = self.execute_remote_command(asset, check_cmd)
            
            return result['success'] and result.get('exit_code', -1) == 0
            
        except Exception as e:
            logger.error(f"Erro ao verificar instalação de {software_name}: {e}")
            return False


class MacOSSoftwareInstaller(BaseSoftwareInstaller):
    """Instalador de software para macOS"""
    
    def __init__(self):
        super().__init__()
        self.supported_software = {
            'Google Chrome': {
                'install_cmd': 'brew install --cask google-chrome',
                'uninstall_cmd': 'brew uninstall --cask google-chrome',
                'check_cmd': 'which google-chrome'
            },
            'Mozilla Firefox': {
                'install_cmd': 'brew install --cask firefox',
                'uninstall_cmd': 'brew uninstall --cask firefox',
                'check_cmd': 'which firefox'
            },
            '7-Zip': {
                'install_cmd': 'brew install p7zip',
                'uninstall_cmd': 'brew uninstall p7zip',
                'check_cmd': 'which 7z'
            },
            'Git': {
                'install_cmd': 'brew install git',
                'uninstall_cmd': 'brew uninstall git',
                'check_cmd': 'which git'
            },
            'Python': {
                'install_cmd': 'brew install python@3.11',
                'uninstall_cmd': 'brew uninstall python@3.11',
                'check_cmd': 'python3 --version'
            },
            'Node.js': {
                'install_cmd': 'brew install node',
                'uninstall_cmd': 'brew uninstall node',
                'check_cmd': 'node --version'
            }
        }
    
    def install_software(self, asset: Asset, software_name: str, version: Optional[str] = None) -> Dict:
        """Instala software no macOS"""
        try:
            if software_name not in self.supported_software:
                return {'success': False, 'error': f'Software não suportado: {software_name}'}
            
            # Verificar se já está instalado
            if self.check_software_installed(asset, software_name):
                return {'success': True, 'message': f'{software_name} já está instalado'}
            
            # Obter comando de instalação
            install_cmd = self.supported_software[software_name]['install_cmd']
            
            # Executar instalação
            result = self.execute_remote_command(asset, install_cmd)
            
            if result['success']:
                return {
                    'success': True,
                    'message': f'{software_name} instalado com sucesso',
                    'details': result
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro ao instalar {software_name}: {result.get("error", "Erro desconhecido")}',
                    'details': result
                }
                
        except Exception as e:
            logger.error(f"Erro ao instalar {software_name} no macOS: {e}")
            return {'success': False, 'error': str(e)}
    
    def uninstall_software(self, asset: Asset, software_name: str, version: Optional[str] = None) -> Dict:
        """Desinstala software no macOS"""
        try:
            if software_name not in self.supported_software:
                return {'success': False, 'error': f'Software não suportado: {software_name}'}
            
            # Verificar se está instalado
            if not self.check_software_installed(asset, software_name):
                return {'success': True, 'message': f'{software_name} não está instalado'}
            
            # Obter comando de desinstalação
            uninstall_cmd = self.supported_software[software_name]['uninstall_cmd']
            
            # Executar desinstalação
            result = self.execute_remote_command(asset, uninstall_cmd)
            
            if result['success']:
                return {
                    'success': True,
                    'message': f'{software_name} desinstalado com sucesso',
                    'details': result
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro ao desinstalar {software_name}: {result.get("error", "Erro desconhecido")}',
                    'details': result
                }
                
        except Exception as e:
            logger.error(f"Erro ao desinstalar {software_name} no macOS: {e}")
            return {'success': False, 'error': str(e)}
    
    def update_software(self, asset: Asset, software_name: str, version: Optional[str] = None) -> Dict:
        """Atualiza software no macOS"""
        try:
            if software_name not in self.supported_software:
                return {'success': False, 'error': f'Software não suportado: {software_name}'}
            
            # Para macOS, usar brew upgrade
            update_cmd = f'brew upgrade {software_name}'
            
            result = self.execute_remote_command(asset, update_cmd)
            
            if result['success']:
                return {
                    'success': True,
                    'message': f'{software_name} atualizado com sucesso',
                    'details': result
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro ao atualizar {software_name}: {result.get("error", "Erro desconhecido")}',
                    'details': result
                }
                
        except Exception as e:
            logger.error(f"Erro ao atualizar {software_name} no macOS: {e}")
            return {'success': False, 'error': str(e)}
    
    def check_software_installed(self, asset: Asset, software_name: str) -> bool:
        """Verifica se software está instalado no macOS"""
        try:
            if software_name not in self.supported_software:
                return False
            
            check_cmd = self.supported_software[software_name]['check_cmd']
            result = self.execute_remote_command(asset, check_cmd)
            
            return result['success'] and result.get('exit_code', -1) == 0
            
        except Exception as e:
            logger.error(f"Erro ao verificar instalação de {software_name}: {e}")
            return False 
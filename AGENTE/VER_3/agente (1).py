import threading, os, subprocess, ctypes, tkinter, time, schedule, logging, wmi, winreg
import platform, socket, uuid, psutil, subprocess, sys, os, json, requests, win32com.client
from datetime import datetime
from pystray import Icon, Menu, MenuItem
from cryptography.fernet import Fernet
from PIL import Image
from urllib.parse import urlparse
import zipfile
import tempfile


# ======= CONFIGURAÇÕES DE CAMINHO =======
def caminho_relativo(*caminho):
    """Retorna o caminho correto independente de estar 'frozen' ou não (PyInstaller)."""
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(__file__)
    return os.path.join(base, *caminho)

# =======   CONSTANTES =======
URL_CHECKIN         = "http://192.168.0.3:5000/checkin"
CAMINHO_PASTA_RAIZ  = r"C:\Program Files\AdvanSee"
CAMINHO_LOG_AGENTE  = os.path.join(CAMINHO_PASTA_RAIZ, "Log")
# =======   CRIPTOGRAFIA =======
ENCRYPTION_KEY      = b'Xexalh4dXCIzMeilnbXok34y5Jx_J5DRP9lR98Yx0rc='
ENCRYPTION_TOKEN    = Fernet(ENCRYPTION_KEY)
# =======   ÍCONES =======
IMAGE_ICON_NORMAL   = Image.open(caminho_relativo("imagens", "uisa_1.png"))
IMAGE_ICON_CHECKIN  = Image.open(caminho_relativo("imagens", "uisa_2.png"))
CREATE_NO_WINDOW    = subprocess.CREATE_NO_WINDOW 

# =======   SERVIDOR =======
AGENT_LISTEN_PORT = 60000
ALLOWED_SERVER_IP = "127.0.0.1"


class AGENTE:
    def __init__(self,):
        pass

    def get_logged_user(self):
        """Obtém o usuário logado usando o comando quser do Windows"""
        try:
            cmd = ['powershell', '-Command', "quser | Select-Object -Skip 1 | ForEach-Object { $_.Trim().Split(' ')[0] }"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, check=True, creationflags=CREATE_NO_WINDOW)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            return None
        except Exception as e:
            logging.error(f"Erro ao obter usuário logado: {e}")
            return None

    def get_system_info(self):
        """Coleta informações detalhadas do sistema"""
        try:
            # Informações básicas do sistema
            system_info = {
                'system_uuid': self.get_system_uuid(),
                'tag': self.get_tag_asset(),
                'hostname': socket.gethostname(),
                'ip_address': self.get_local_ip(),
                'mac_address': self.get_mac_address(),
                'operating_system': f"{platform.system()} {platform.release()}",
                'os_version': platform.version(),
                'architecture': platform.architecture()[0],
                'processor': platform.processor(),
                'logged_user': self.get_logged_user(),
                'python_version': platform.python_version(),
            }

            # Informações de hardware
            system_info.update(self.get_hardware_info())

            # Software instalado
            system_info['installed_software'] = self.get_installed_software()

            # Informações de rede
            system_info['network_interfaces'] = self.get_network_interfaces()

            # Informações de disco
            system_info['disk_info'] = self.get_disk_info()

            # Informações de memória
            system_info['memory_info'] = self.get_memory_info()

            # Processos em execução (limitado)
            system_info['running_processes'] = self.get_running_processes()

            # Serviços do Windows (se aplicável)
            if platform.system() == 'Windows':
                system_info['windows_services'] = self.get_windows_services()
                system_info['windows_updates'] = self.get_windows_updates()

            return system_info

        except Exception as e:
            logging.error(f"Erro ao coletar informações do sistema: {e}")
            return {}

    def get_tag_asset(self):
        """Obtém a tag do asset"""
        #Get-WmiObject Win32_BIOS | Select-Object SerialNumber
        try:
            cmd = ['powershell', '-Command', "Get-WmiObject Win32_BIOS | Select-Object SerialNumber"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, check=True, creationflags=CREATE_NO_WINDOW)
            return result.stdout.strip().split('\n')[2]
        except Exception as e:
            logging.warning(f"Erro ao obter tag do asset: {e}")
            return None

    def get_system_uuid(self):
        """Obtém um UUID persistente do sistema (placa-mãe ou VM UUID) para Windows e Linux."""
        system_os = platform.system()
        print("get_system_uuid")
        try:
            if system_os == 'Windows':
                # Usar PowerShell para obter o UUID da BIOS/UEFI ou VM UUID
                # Get-CimInstance é o cmdlet moderno para WMI
                cmd = ['powershell', '-Command', '(Get-CimInstance -ClassName Win32_ComputerSystemProduct).UUID']
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, check=True, creationflags=CREATE_NO_WINDOW)
                if result.returncode == 0:
                    uuid_val = result.stdout.strip()
                    if uuid_val and uuid_val != "00000000-0000-0000-0000-000000000000":
                        return uuid_val
            elif system_os == 'Linux':
                # Tentar product_uuid do DMI (geralmente UUID da placa-mãe)
                try:
                    with open('/sys/class/dmi/id/product_uuid', 'r') as f:
                        uuid_val = f.read().strip()
                        if uuid_val and uuid_val != "00000000-0000-0000-0000-000000000000":
                            return uuid_val
                except FileNotFoundError:
                    pass # Fallback para UUID do disco se DMI não estiver disponível

                # Fallback: Obter UUID da partição raiz (ajuste conforme necessário para sua configuração)
                # Note: 'sudo' pode ser necessário dependendo das permissões do usuário que executa o agente.
                # Para evitar sudo, considere usar psutil para obter informações de disco e depois buscar o UUID.
                # Simplificado aqui para demonstração.
                cmd = ['blkid', '-o', 'value', '-s', 'UUID', '/dev/sda1'] # Assumes /dev/sda1 is root
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, check=True, creationflags=CREATE_NO_WINDOW)
                if result.returncode == 0:
                    return result.stdout.strip()
            # Adicionar macOS ou outros OS, se necessário
            # elif system_os == 'Darwin':
            #     cmd = ['ioreg', '-rd1', '-c', 'IOPlatformExpertDevice']
            #     result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            #     # ... parse output for IOPlatformUUID ...

        except subprocess.CalledProcessError as e:
            logging.warning(f"Comando para obter UUID falhou com código de saída {e.returncode}: {e.stderr.strip()}")
        except Exception as e:
            logging.warning(f"Não foi possível obter um UUID de sistema persistente: {e}")
        return None

    def get_local_ip(self):
        """Obtém o IP local da máquina"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return socket.gethostbyname(socket.gethostname())

    def get_mac_address(self):
        """Obtém o endereço MAC da máquina"""
        mac = uuid.getnode()
        return ':'.join(['{:02x}'.format((mac >> elements) & 0xff)
                        for elements in range(0, 2*6, 2)][::-1])

    def get_hardware_info(self):
        """Coleta informações de hardware usando psutil"""
        try:
            cpu_info = {
                'cpu_count': psutil.cpu_count(),
                'cpu_count_logical': psutil.cpu_count(logical=True),
                'cpu_freq_current': psutil.cpu_freq().current if psutil.cpu_freq() else None,
                'cpu_freq_min': psutil.cpu_freq().min if psutil.cpu_freq() else None,
                'cpu_freq_max': psutil.cpu_freq().max if psutil.cpu_freq() else None,
            }

            memory = psutil.virtual_memory()
            memory_info = {
                'total_memory_bytes': memory.total,
                'available_memory_bytes': memory.available,
                'memory_percent': memory.percent,
            }

            # Obter informações do modelo e fabricante do equipamento
            computer_info = self.get_computer_model_info()

            return {**cpu_info, **memory_info, **computer_info}
        except Exception as e:
            logging.error(f"Erro ao coletar informações de hardware: {e}")
            return {}

    def get_computer_model_info(self):
        """Obtém informações do modelo e fabricante do computador"""
        try:
            computer_info = {}
            
            if platform.system() == 'Windows':
                # Usar WMI para obter informações do sistema
                c = wmi.WMI()
                
                # Informações do sistema
                for system in c.Win32_ComputerSystem():
                    computer_info['computer_model'] = system.Model.strip() if system.Model else None
                    computer_info['computer_manufacturer'] = system.Manufacturer.strip() if system.Manufacturer else None
                    computer_info['computer_system_type'] = system.SystemType.strip() if system.SystemType else None
                    break
                
                # Informações adicionais da placa-mãe
                for board in c.Win32_BaseBoard():
                    if board.Manufacturer and not computer_info.get('computer_manufacturer'):
                        computer_info['computer_manufacturer'] = board.Manufacturer.strip()
                    if board.Product and not computer_info.get('computer_model'):
                        computer_info['computer_model'] = board.Product.strip()
                    break
                
                # Informações do BIOS
                for bios in c.Win32_BIOS():
                    if bios.Manufacturer and not computer_info.get('computer_manufacturer'):
                        computer_info['computer_manufacturer'] = bios.Manufacturer.strip()
                    break
                    
            elif platform.system() == 'Linux':
                # Para Linux, tentar ler informações do DMI
                try:
                    with open('/sys/class/dmi/id/sys_vendor', 'r') as f:
                        computer_info['computer_manufacturer'] = f.read().strip()
                except FileNotFoundError:
                    pass
                
                try:
                    with open('/sys/class/dmi/id/product_name', 'r') as f:
                        computer_info['computer_model'] = f.read().strip()
                except FileNotFoundError:
                    pass
                    
            elif platform.system() == 'Darwin':  # macOS
                try:
                    # Usar system_profiler para obter informações do hardware
                    cmd = ['system_profiler', 'SPHardwareDataType']
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, creationflags=CREATE_NO_WINDOW)
                    
                    if result.returncode == 0:
                        output = result.stdout
                        for line in output.split('\n'):
                            if 'Model Name:' in line:
                                computer_info['computer_model'] = line.split(':', 1)[1].strip()
                            elif 'Model Identifier:' in line:
                                if not computer_info.get('computer_model'):
                                    computer_info['computer_model'] = line.split(':', 1)[1].strip()
                            elif 'Manufacturer:' in line:
                                computer_info['computer_manufacturer'] = line.split(':', 1)[1].strip()
                except Exception as e:
                    logging.warning(f"Erro ao obter informações do hardware no macOS: {e}")
            
            return computer_info
            
        except Exception as e:
            logging.error(f"Erro ao obter informações do modelo do computador: {e}")
            return {}

    def get_installed_software(self):
        """Obtém a lista de programas instalados no Windows."""
        software_list = []
    
        paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        
        for path in paths:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                try:
                                    software_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                    software_version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                                    software_vendor = winreg.QueryValueEx(subkey, "Publisher")[0]
                                    software_list.append({
                                        "Name": software_name.strip(),
                                        "Version": software_version.strip(),
                                        "Vendor": software_vendor.strip()
                                    })
                                except (WindowsError, KeyError):
                                    continue
                        except WindowsError:
                            continue
            except WindowsError:
                continue
        
        return software_list

    def get_network_interfaces(self):
        """Obtém informações das interfaces de rede"""
        try:
            interfaces = []
            for interface, addrs in psutil.net_if_addrs().items():
                interface_info = {'name': interface, 'addresses': []}
                for addr in addrs:
                    interface_info['addresses'].append({
                        'family': str(addr.family),
                        'address': addr.address,
                        'netmask': addr.netmask,
                        'broadcast': addr.broadcast
                    })
                interfaces.append(interface_info)
            return interfaces
        except Exception as e:
            logging.error(f"Erro ao obter interfaces de rede: {e}")
            return []

    def get_disk_info(self):
        disks = []
        c = wmi.WMI()
        try:
            # Obter informações físicas dos discos
            for physical_disk in c.Win32_DiskDrive():
                for partition in psutil.disk_partitions():
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        disks.append({
                            'device': partition.device,
                            'mountpoint': partition.mountpoint,
                            'fstype': partition.fstype,
                            'total_bytes': usage.total,
                            'used_bytes': usage.used,
                            'free_bytes': usage.free,
                            'percent': usage.percent,
                            'model': physical_disk.Model,
                            'serial': physical_disk.SerialNumber.strip(),
                            'interface_type': physical_disk.InterfaceType
                        })
                    except PermissionError:
                        return disks
        except Exception as e:
            logging.error(f"Erro ao obter informações de disco: {e}")
            return disks
    
    def get_memory_info(self):
        """Obtém informações detalhadas da memória RAM"""

        def _get_ram_type(memory_type):
            """Mapeia códigos de tipo de memória para descrições legíveis"""
            ram_types = {
                0: "Unknown",
                1: "Other",
                2: "DRAM",
                3: "Synchronous DRAM",
                4: "Cache DRAM",
                5: "EDO",
                6: "EDRAM",
                7: "VRAM",
                8: "SRAM",
                9: "RAM",
                10: "ROM",
                11: "Flash",
                12: "EEPROM",
                13: "FEPROM",
                14: "EPROM",
                15: "CDRAM",
                16: "3DRAM",
                17: "SDRAM",
                18: "SGRAM",
                19: "RDRAM",
                20: "DDR",
                21: "DDR2",
                22: "DDR2 FB-DIMM",
                24: "DDR3",
                25: "FBD2",
                26: "DDR4",
                27: "LPDDR",
                28: "LPDDR2",
                29: "LPDDR3",
                30: "LPDDR4",
                31: "DDR5",
                32: "LPDDR5",
                33: "DDR6",
                34: "LPDDR6",
                # Adicionando alguns tipos menos comuns para completar
                35: "HBM",
                36: "HBM2",
                37: "HBM3",
                38: "GDDR",
                39: "GDDR2",
                40: "GDDR3",
                41: "GDDR4",
                42: "GDDR5",
                43: "GDDR5X",
                44: "GDDR6",
                45: "GDDR6X",
                46: "GDDR7"
            }
            return ram_types.get(memory_type, f"Unknown ({memory_type})")

        def _get_form_factor(form_factor):
            """Mapeia códigos de fator de forma para descrições legíveis"""
            form_factors = {
                0: "Unknown",
                1: "Other",
                2: "SIP",
                3: "DIP",
                4: "ZIP",
                5: "SOJ",
                6: "Proprietary",
                7: "SIMM",
                8: "DIMM",
                9: "TSOP",
                10: "PGA",
                11: "RIMM",
                12: "SODIMM",
                13: "SRIMM",
                14: "SMD",
                15: "SSMP",
                16: "QFP",
                17: "TQFP",
                18: "SOIC",
                19: "LCC",
                20: "PLCC",
                21: "BGA",
                22: "FPBGA",
                23: "LGA"
            }
            return form_factors.get(form_factor, f"Unknown ({form_factor})")

        def _get_windows_ram_details():
            """Obtém detalhes da RAM no Windows usando WMI"""
            try:
                import wmi
                c = wmi.WMI()
                modules = []
                for mem in c.Win32_PhysicalMemory():
                    module = {
                        'manufacturer': mem.Manufacturer,
                        'part_number': mem.PartNumber.strip(),
                        'serial': mem.SerialNumber.strip(),
                        'capacity_bytes': int(mem.Capacity),
                        'speed_mhz': mem.Speed,
                        'memory_type': _get_ram_type(mem.MemoryType),
                        'form_factor': _get_form_factor(mem.FormFactor)
                    }
                    modules.append(module)

                return modules
            except Exception as e:
                logging.error(f"Erro ao obter detalhes da RAM no Windows: {e}")
                return []

        try:
            ram_info = {
                'total_bytes': psutil.virtual_memory().total,
                'available_bytes': psutil.virtual_memory().available,
                'used_bytes': psutil.virtual_memory().used,
                'percent': psutil.virtual_memory().percent,
                'modules': []
            }
            ram_info['modules'] = _get_windows_ram_details()
            return ram_info
        except Exception as e:
            logging.error(f"Erro ao obter informações de RAM: {e}")
            return {}

    def get_running_processes(self):
        """Lista processos em execução (limitado aos principais)"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            return processes[:20]
        except Exception as e:
            logging.error(f"Erro ao listar processos: {e}")
            return []

    def get_windows_services(self):
        """Lista serviços do Windows"""
        if platform.system() != 'Windows':
            return []

        try:
            cmd = 'Get-Service | Select-Object Name, Status, StartType | ConvertTo-Json'
            result = subprocess.run(['powershell', '-Command', cmd],
                                  capture_output=True, text=True, timeout=30, creationflags=CREATE_NO_WINDOW)

            if result.returncode == 0 and result.stdout:
                services_data = json.loads(result.stdout)
                if isinstance(services_data, list):
                    return services_data[:50]
                elif isinstance(services_data, dict):
                    return [services_data]
        except Exception as e:
            logging.error(f"Erro ao listar serviços do Windows: {e}")

        return []

    def get_windows_updates(self):
        try:
            # Conecta ao WMI
            wmi = win32com.client.GetObject("winmgmts:")
            updates = wmi.ExecQuery("SELECT * FROM Win32_QuickFixEngineering")  # KB updates
            
            updates_list = []
            for update in updates:
                updates_list.append({
                    "HotFixID": update.HotFixID,               # Exemplo: "KB5034441"
                    "Description": update.Description,         # Descrição (às vezes vazio)
                    "InstalledOn": update.InstalledOn,         # Data de instalação
                    "InstalledBy": update.InstalledBy          # Usuário/processo que instalou
                })
            
            return {
                "updates": updates_list,
                "count": len(updates_list)
            }
        
        except Exception as e:
            return {"error": str(e)}

    def get_battery_info(self):
        battery = psutil.sensors_battery()
        if not battery:
            return {"error": "Bateria não detectada"}

        w = wmi.WMI()
        battery_wmi = w.Win32_Battery()[0]

        battery_info = {
            "percent": battery.percent,
            "power_plugged": battery.power_plugged,
            "status": "Carregando" if battery.power_plugged else "Descarregando",
            "design_capacity": getattr(battery_wmi, "DesignCapacity", "Desconhecido"),
            "full_charge_capacity": getattr(battery_wmi, "FullChargeCapacity", "Desconhecido"),
            "cycle_count": getattr(battery_wmi, "CycleCount", "Desconhecido"),
            "battery_name": getattr(battery_wmi, "Name", "Desconhecido"),
            "DeviceID": getattr(battery_wmi,"DeviceID","Desconhecido")
        }
        return battery_info

class ADVANSEE:
    def __init__(self):
        self.icon = Icon("Monitorar")
        self.stop_event = threading.Event()

    def icon_bar(self):
        self.icon.icon = IMAGE_ICON_NORMAL
        self.icon.menu = Menu(
            MenuItem("Sair", self.Icon_sair),
            MenuItem("CheckIn", self.Monitorar)
            )

        self.icon.run()

    def Icon_sair(self, icon, item):
        logging.info("Agente interrompido pelo usuário")
        self.stop_event.set()
        self.icon.stop()
        exit()
        sys.exit()
        

    def update_gpo(self):
        try:
            # Executa o gpupdate /force para atualizar todas as políticas
            result = subprocess.run(['gpupdate', '/force'], 
                                capture_output=True, 
                                text=True, 
                                check=True)
            print("GPO atualizado com sucesso!")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print("Erro ao atualizar GPO:")
            print(e.stderr)

    def force_reboot(self):
        """Força o reinício do sistema"""
        try:
            result = subprocess.run(['shutdown', '/r', '/t', '0', '/f'],
                                  capture_output=True, text=True, creationflags=CREATE_NO_WINDOW)
            return {"status": "success", "message": "Reinício iniciado"}
        except Exception as e:
            return {"status": "error", "message": f"Erro ao reiniciar: {str(e)}"}

    def download_and_install_file(self, url, filename=None):
        """
        Função para baixar e instalar um arquivo
        """
        try:
            logging.info(f"Iniciando download de: {url}")
            
            # Fazer download do arquivo
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Determinar nome do arquivo
            if not filename:
                # Extrair nome do arquivo da URL
                parsed_url = urlparse(url)
                filename = os.path.basename(parsed_url.path)
                if not filename:
                    filename = "downloaded_file"
            
            # Criar pasta temporária para download
            temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(temp_dir, filename)
            
            # Salvar arquivo
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logging.info(f"Arquivo baixado: {file_path}")
            
            # Verificar tipo de arquivo e instalar
            file_extension = os.path.splitext(filename)[1].lower()
            
            if file_extension == '.msi':
                return self.install_msi_file(file_path)
            elif file_extension == '.exe':
                return self.install_exe_file(file_path)
            elif file_extension == '.zip':
                return self.extract_zip_file(file_path, temp_dir)
            elif file_extension == '.msu':
                return self.install_msu_file(file_path)
            else:
                logging.warning(f"Tipo de arquivo não suportado: {file_extension}")
                return {
                    "status": "warning",
                    "message": f"Arquivo baixado mas tipo não suportado: {file_extension}"
                }
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro no download: {e}")
            return {
                "status": "error",
                "message": f"Erro no download: {str(e)}"
            }
        except Exception as e:
            logging.error(f"Erro inesperado: {e}")
            return {
                "status": "error",
                "message": f"Erro inesperado: {str(e)}"
            }

    def install_msi_file(self, file_path):
        """Instala arquivo MSI"""
        try:
            logging.info(f"Instalando MSI: {file_path}")
            
            # Comando para instalar MSI silenciosamente
            cmd = [
                'msiexec',
                '/i', file_path,
                '/quiet',
                '/norestart',
                '/log', f"{file_path}.log"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutos
                creationflags=CREATE_NO_WINDOW
            )
            
            if result.returncode == 0:
                logging.info("MSI instalado com sucesso")
                return {
                    "status": "success",
                    "message": "MSI instalado com sucesso"
                }
            else:
                logging.error(f"Erro na instalação MSI: {result.stderr}")
                return {
                    "status": "error",
                    "message": f"Erro na instalação MSI: {result.stderr}"
                }
        
        except subprocess.TimeoutExpired:
            logging.error("Timeout na instalação MSI")
            return {
                "status": "error",
                "message": "Timeout na instalação MSI"
            }
        except Exception as e:
            logging.error(f"Erro inesperado na instalação MSI: {e}")
            return {
                "status": "error",
                "message": f"Erro inesperado na instalação MSI: {str(e)}"
            }

    def install_exe_file(self, file_path):
        """Instala arquivo EXE"""
        try:
            logging.info(f"Executando EXE: {file_path}")
            
            # Comando para executar EXE silenciosamente
            cmd = [
                file_path,
                '/S',  # Silent install
                '/quiet',
                '/norestart'
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutos
                creationflags=CREATE_NO_WINDOW
            )
            
            if result.returncode == 0:
                logging.info("EXE executado com sucesso")
                return {
                    "status": "success",
                    "message": "EXE executado com sucesso"
                }
            else:
                logging.error(f"Erro na execução EXE: {result.stderr}")
                return {
                    "status": "error",
                    "message": f"Erro na execução EXE: {result.stderr}"
                }
        
        except subprocess.TimeoutExpired:
            logging.error("Timeout na execução EXE")
            return {
                "status": "error",
                "message": "Timeout na execução EXE"
            }
        except Exception as e:
            logging.error(f"Erro inesperado na execução EXE: {e}")
            return {
                "status": "error",
                "message": f"Erro inesperado na execução EXE: {str(e)}"
            }

    def extract_zip_file(self, file_path, extract_dir):
        """Extrai arquivo ZIP"""
        try:
            logging.info(f"Extraindo ZIP: {file_path}")
            
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            logging.info(f"ZIP extraído para: {extract_dir}")
            return {
                "status": "success",
                "message": f"ZIP extraído com sucesso para {extract_dir}"
            }
        
        except Exception as e:
            logging.error(f"Erro na extração ZIP: {e}")
            return {
                "status": "error",
                "message": f"Erro na extração ZIP: {str(e)}"
            }

    def install_msu_file(self, file_path):
        """Instala arquivo MSU (Windows Update)"""
        try:
            logging.info(f"Instalando MSU: {file_path}")
            
            # Comando para instalar MSU
            cmd = [
                'wusa.exe',
                file_path,
                '/quiet',
                '/norestart'
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutos
                creationflags=CREATE_NO_WINDOW
            )
            
            if result.returncode == 0:
                logging.info("MSU instalado com sucesso")
                return {
                    "status": "success",
                    "message": "MSU instalado com sucesso"
                }
            else:
                logging.error(f"Erro na instalação MSU: {result.stderr}")
                return {
                    "status": "error",
                    "message": f"Erro na instalação MSU: {result.stderr}"
                }
        
        except subprocess.TimeoutExpired:
            logging.error("Timeout na instalação MSU")
            return {
                "status": "error",
                "message": "Timeout na instalação MSU"
            }
        except Exception as e:
            logging.error(f"Erro inesperado na instalação MSU: {e}")
            return {
                "status": "error",
                "message": f"Erro inesperado na instalação MSU: {str(e)}"
            }

    def handle_download_and_install_command(self, command_data):
        """
        Função para processar comando DOWNLOAD_AND_INSTALL
        """
        try:
            # O comando vem com estrutura: {'command': 'DOWNLOAD_AND_INSTALL', 'data': {'url': '...', 'filename': '...'}}
            data = command_data.get('data', {})
            url = data.get('url')
            filename = data.get('filename')
            
            logging.info(f"Comando DOWNLOAD_AND_INSTALL recebido - URL: {url}, Filename: {filename}")
            
            if not url:
                return {
                    "status": "error",
                    "message": "URL não fornecida"
                }
            
            result = self.download_and_install_file(url, filename)
            
            return result
        
        except Exception as e:
            logging.error(f"Erro no comando DOWNLOAD_AND_INSTALL: {e}")
            return {
                "status": "error",
                "message": f"Erro interno: {str(e)}"
            }

    def Monitorar(self):
        self.agente = AGENTE()
        self.icon.icon  = IMAGE_ICON_CHECKIN
        system_info = self.agente.get_system_info()

        # Garante que o system_uuid esteja disponível antes de prosseguir
        if not system_info.get('system_uuid'):
            logging.error("Não foi possível obter o UUID do sistema. Abortando check-in.")
            self.icon.icon = IMAGE_ICON_NORMAL
            return

        pacote = {
            'asset_tag': system_info["system_uuid"], # Usando system_uuid como asset_tag
            'agent_version': "0.0.0.1",
            'system_info': system_info,
            'timestamp': datetime.now().isoformat()
        }
        caminho_completo = os.path.join(CAMINHO_LOG_AGENTE, "pacote.txt")
        with open(caminho_completo, 'w') as f:
            json.dump(pacote, f, indent=4)

        try:
            json_data = json.dumps(pacote).encode('utf-8')
            pacote_criptografado = ENCRYPTION_TOKEN.encrypt(json_data)

            pacote_encriptografado_para_servidor = {
                "encrypted_payload": pacote_criptografado.decode('latin-1') # Decodificar para string para enviar em JSON
            }


            logging.info(f"Realizando check-in para ativo {system_info['system_uuid']}")
            response = requests.post(URL_CHECKIN, json=pacote_encriptografado_para_servidor, timeout=30)
            if response.status_code == 200:
                logging.info(f"Check-in realizado com sucesso: {response.status_code}")
                resposta_servidor = response.json()
                logging.info(f"Resposta do Servidor: {resposta_servidor}")
            else:
                logging.error(f"Erro no check-in: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
                logging.error(f"Erro de conexão durante check-in: {e}")
        except Exception as e:
                logging.error(f"Erro inesperado durante check-in: {e}")
        self.icon.icon = IMAGE_ICON_NORMAL

    def start_command_listener(self):
        """Inicia um servidor de socket para escutar comandos do servidor central."""
        HOST = '0.0.0.0'  # Escuta em todas as interfaces
        PORT = AGENT_LISTEN_PORT

        try:
            self.agent_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.agent_socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.agent_socket_server.bind((HOST, PORT))
            self.agent_socket_server.listen(5)
            logging.info(f"Agente escutando por comandos em {HOST}:{PORT}")

            while not self.stop_event.is_set():
                try:
                    self.agent_socket_server.settimeout(1.0) # Tempo limite para que a thread possa verificar stop_event
                    conn, addr = self.agent_socket_server.accept()
                    if addr[0] == ALLOWED_SERVER_IP:
                        logging.info(f"Conexão aceita de {addr[0]}")
                        threading.Thread(target=self.handle_client_command, args=(conn, addr)).start()
                    else:
                        logging.warning(f"Conexão recusada de IP não autorizado: {addr[0]}")
                        conn.close()
                except socket.timeout:
                    continue # Continua o loop para verificar stop_event
                except Exception as e:
                    if self.stop_event.is_set(): # Se a parada foi solicitada, ignora o erro
                        break
                    logging.error(f"Erro ao aceitar conexão de comando: {e}")
        except Exception as e:
            logging.error(f"Falha ao iniciar o servidor de comandos do agente: {e}")

    def handle_client_command(self, conn, addr):
        """Lida com comandos recebidos do servidor."""
        try:
            data_raw = conn.recv(4096) # Recebe os dados brutos (criptografados)
            if not data_raw:
                return

            logging.info(f"Dados recebidos de {addr[0]}: {data_raw}")

            try:
                decrypted_data_bytes = ENCRYPTION_TOKEN.decrypt(data_raw)
                command_data = json.loads(decrypted_data_bytes.decode('utf-8'))
                logging.info(f"Comando descriptografado: {command_data}")
                
                response_payload = {"status": "error", "message": "Comando não reconhecido"}
                
                # Processa diferentes tipos de comandos
                if isinstance(command_data, str):
                    if command_data == 'FORCE_CHECKIN':
                        logging.info("COMANDO FORCE_CHECKIN RECEBIDO PELO AGENTE")
                        self.update_gpo()
                        response_payload = {"status": "success", "message": "GPO atualizado com sucesso"}
                    
                    elif command_data == 'CHECK_UPDATES':
                        logging.info("COMANDO CHECK_UPDATES RECEBIDO PELO AGENTE")
                        result = self.check_windows_updates_available()
                        response_payload = result
                    
                    elif command_data == 'INSTALL_ALL_UPDATES':
                        logging.info("COMANDO INSTALL_ALL_UPDATES RECEBIDO PELO AGENTE")
                        result = self.install_all_windows_updates()
                        response_payload = result
                    
                    elif command_data == 'FORCE_REBOOT':
                        logging.info("COMANDO FORCE_REBOOT RECEBIDO PELO AGENTE")
                        result = self.force_reboot()
                        response_payload = result
                
                elif isinstance(command_data, dict):
                    if command_data.get('command') == 'INSTALL_KB':
                        kb_number = command_data.get('kb_number')
                        if kb_number:
                            logging.info(f"COMANDO INSTALL_KB RECEBIDO PELO AGENTE: {kb_number}")
                            result = self.install_specific_kb(kb_number)
                            response_payload = result
                        else:
                            response_payload = {"status": "error", "message": "Número KB não fornecido"}
                    
                    elif command_data.get('command') == 'CHECK_UPDATES':
                        logging.info("COMANDO CHECK_UPDATES RECEBIDO PELO AGENTE")
                        result = self.check_windows_updates_available()
                        response_payload = result
                    
                    elif command_data.get('command') == 'INSTALL_ALL_UPDATES':
                        logging.info("COMANDO INSTALL_ALL_UPDATES RECEBIDO PELO AGENTE")
                        result = self.install_all_windows_updates()
                        response_payload = result
                    
                    elif command_data.get('command') == 'FORCE_REBOOT':
                        logging.info("COMANDO FORCE_REBOOT RECEBIDO PELO AGENTE")
                        result = self.force_reboot()
                        response_payload = result
                    
                    elif command_data.get('command') == 'DOWNLOAD_AND_INSTALL':
                        logging.info("COMANDO DOWNLOAD_AND_INSTALL RECEBIDO PELO AGENTE")
                        result = self.handle_download_and_install_command(command_data)
                        response_payload = result
                
                # Envia resposta de volta ao servidor
                try:
                    response_json = json.dumps(response_payload).encode('utf-8')
                    response_encrypted = ENCRYPTION_TOKEN.encrypt(response_json)
                    conn.send(response_encrypted)
                    logging.info(f"Resposta enviada para {addr[0]}: {response_payload}")
                except Exception as e:
                    logging.error(f"Erro ao enviar resposta para {addr[0]}: {e}")
                    
            except Exception as e:
                logging.error(f"Erro ao descriptografar ou processar comando: {e}")
                response_payload = {"status": "error", "message": f"Erro interno do agente: {e}"}
                try:
                    response_json = json.dumps(response_payload).encode('utf-8')
                    response_encrypted = ENCRYPTION_TOKEN.encrypt(response_json)
                    conn.send(response_encrypted)
                except:
                    pass
        except Exception as e:
            logging.error(f"Erro ao lidar com cliente de comando {addr[0]}: {e}")
        finally:
            conn.close()
            logging.info(f"Conexão com {addr[0]} fechada.")


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def CriarPasta():
    if not is_admin():
        # Reexecuta o script com privilégios de administrador
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, ' '.join(sys.argv), None, 0)
        sys.exit()
    if not os.path.exists(CAMINHO_PASTA_RAIZ):
        os.makedirs(CAMINHO_PASTA_RAIZ)
        subprocess.run(f'icacls "{CAMINHO_PASTA_RAIZ}" /inheritance:r', shell=True, creationflags=CREATE_NO_WINDOW)
        subprocess.run(f'icacls "{CAMINHO_PASTA_RAIZ}" /grant:r Administradores:F', shell=True, creationflags=CREATE_NO_WINDOW)
        subprocess.run(f'icacls "{CAMINHO_PASTA_RAIZ}" /deny Users:(W,RD,WDAC,WO)', shell=True, creationflags=CREATE_NO_WINDOW)
    if not os.path.exists(CAMINHO_LOG_AGENTE):
        os.makedirs(CAMINHO_LOG_AGENTE)
        subprocess.run(f'icacls "{CAMINHO_LOG_AGENTE}" /inheritance:r', shell=True, creationflags=CREATE_NO_WINDOW)
        subprocess.run(f'icacls "{CAMINHO_LOG_AGENTE}" /grant:r Administradores:F', shell=True, creationflags=CREATE_NO_WINDOW)
        subprocess.run(f'icacls "{CAMINHO_LOG_AGENTE}" /deny Users:(W,RD,WDAC,WO)', shell=True, creationflags=CREATE_NO_WINDOW)

    log_file_path = os.path.join(CAMINHO_LOG_AGENTE, "agente.log")
    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
        ]
    )

def main():
    CriarPasta()
    advansee = ADVANSEE()

    command_listener_thread = threading.Thread(target=advansee.start_command_listener, daemon=True)
    command_listener_thread.start()
    icon_thread = threading.Thread(target=advansee.icon_bar, daemon=True)
    icon_thread.start()

    # Agenda a função Monitorar para ser executada a cada 5 minutos
    schedule.every(5).minutes.do(advansee.Monitorar)
    while not advansee.stop_event.is_set():
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
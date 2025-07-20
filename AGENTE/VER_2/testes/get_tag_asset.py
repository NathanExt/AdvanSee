import subprocess
import logging


CREATE_NO_WINDOW    = subprocess.CREATE_NO_WINDOW

def get_tag_asset():
    """Obtém a tag do asset"""
    #Get-WmiObject Win32_BIOS | Select-Object SerialNumber
    try:
        cmd = ['powershell', '-Command', "Get-WmiObject Win32_BIOS | Select-Object SerialNumber"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, check=True, creationflags=CREATE_NO_WINDOW)
        return result.stdout.strip().split('\n')[2]
    except Exception as e:
        print(e)



def main():
    a = get_tag_asset()
    print(a)

main()
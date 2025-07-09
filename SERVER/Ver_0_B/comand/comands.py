import socket, json
from cryptography.fernet import Fernet
from config import Config

# A MESMA CHAVE DEVE SER USADA AQUI
SERVER_ENCRYPTION_KEY = Config.ENCRYPTION_KEY
SERVER_TOKEN_SUITE = Fernet(SERVER_ENCRYPTION_KEY)
AGENT_PORT = Config.AGENT_LISTEN_PORT

class COMANDOS:
    def __init__(self):
        pass

    def send_command_to_agent(command_payload,AGENT_IP):
        print(command_payload)
        print(AGENT_IP)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((AGENT_IP, AGENT_PORT))
                
                # Criptografa o comando
                json_command = json.dumps(command_payload).encode('utf-8')
                encrypted_command = SERVER_TOKEN_SUITE.encrypt(json_command)
                
                s.sendall(encrypted_command)
                
                # Recebe e descriptografa a resposta
                encrypted_response = s.recv(4096)
                if encrypted_response:
                    decrypted_response_bytes = SERVER_TOKEN_SUITE.decrypt(encrypted_response)
                    response_data = json.loads(decrypted_response_bytes.decode('utf-8'))
                    print("Resposta do agente:", response_data)
                    return response_data
                else:
                    print("Nenhuma resposta do agente.")

        except Exception as e:
            print(f"Erro ao enviar comando para o agente: {e}") 
import socket, json, logging
from cryptography.fernet import Fernet
from config import CONFIG

# A MESMA CHAVE DEVE SER USADA AQUI
SERVER_ENCRYPTION_KEY = CONFIG.ENCRYPTION_KEY
SERVER_TOKEN_SUITE = Fernet(SERVER_ENCRYPTION_KEY)
AGENT_PORT = CONFIG.AGENT_LISTEN_PORT

logging.basicConfig(level=logging.INFO)

class COMANDOS:
    def __init__(self):
        pass

    def send_command_to_agent(self,command_payload,AGENT_IP):
        logging.info(f"send_command_to_agent")
        logging.info(f"IP do agente: {AGENT_IP}")
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
                    logging.info(f"Resposta do agente: {response_data}")
                    return response_data
                else:
                    logging.error("Nenhuma resposta do agente.")
                    return None

        except Exception as e:
            logging.error(f"Erro ao enviar comando para o agente: {e}") 
# AdvanSee - Sistema de Gestão de Inventário Automatizado

## Instalação e Configuração

### Pré-requisitos

- **Python 3.8+** (recomendado Python 3.11)
- **PostgreSQL 12+** 
- **Git**

### 1. Clone do Repositório

```bash
git clone <url-do-repositorio>
cd AdvanSee
```

### 2. Configuração do Ambiente Virtual

#### Windows
```bash
# Criar ambiente virtual
python -m venv venv_advansee

# Ativar ambiente virtual
venv_advansee\Scripts\activate

# Ou no PowerShell
venv_advansee\Scripts\Activate.ps1
```

#### Linux/macOS
```bash
# Criar ambiente virtual
python3 -m venv venv_advansee

# Ativar ambiente virtual
source venv_advansee/bin/activate
```

### 3. Instalação das Dependências

#### Para o Servidor (Flask)
```bash
cd SERVER/Ver_0_B
pip install -r requirements.txt
```

#### Para o Agente
```bash
cd AGENTE
pip install -r requirements.txt
```

#### Instalação Mínima (apenas servidor)
```bash
cd SERVER/Ver_0_B
pip install -r requirements-minimal.txt
```

### 4. Configuração do Banco de Dados

#### 4.1. Criar Bancos de Dados
```sql
-- Banco principal
CREATE DATABASE ISAC_BD_ADVANSEE_2;

-- Banco PMOC
CREATE DATABASE BD_PMOC;

-- Criar usuário (se necessário)
CREATE USER isac WITH PASSWORD 'kwa44fgjc8suf91kjsacaz';
GRANT ALL PRIVILEGES ON DATABASE ISAC_BD_ADVANSEE_2 TO isac;
GRANT ALL PRIVILEGES ON DATABASE BD_PMOC TO isac;
```

#### 4.2. Executar Scripts de Migração
```bash
cd SERVER/Ver_0_B

# Atualizar esquema do banco principal
python update_database_schema.py

# Executar script SQL para adicionar colunas de informações do computador
psql -U isac -d ISAC_BD_ADVANSEE_2 -f add_computer_info_columns.sql
```

### 5. Configuração do Servidor

#### 5.1. Verificar Configurações
Edite o arquivo `SERVER/Ver_0_B/config.py` se necessário:

```python
# Configurações do banco
DB_HOST = "127.0.0.1"
DB_USER = "isac"
DB_PASSWORD = "kwa44fgjc8suf91kjsacaz"
DB_PORT = "5432"
```

#### 5.2. Iniciar o Servidor
```bash
cd SERVER/Ver_0_B
python app.py
```

O servidor estará disponível em: `http://localhost:5000`

### 6. Configuração do Agente

#### 6.1. Configurar URL do Servidor
Edite o arquivo `AGENTE/agente.py`:

```python
URL_CHECKIN = "http://127.0.0.1:5000/checkin"  # URL do seu servidor
```

#### 6.2. Executar o Agente
```bash
cd AGENTE
python agente.py
```

### 7. Testes

#### 7.1. Testar Servidor
```bash
cd SERVER/Ver_0_B
python test_computer_info.py
```

#### 7.2. Testar Conexão com Banco
```bash
cd SERVER/Ver_0_B
python update_database_schema.py
```

## Estrutura do Projeto

```
AdvanSee/
├── AGENTE/                    # Agente de coleta de informações
│   ├── agente.py             # Script principal do agente
│   ├── requirements.txt      # Dependências do agente
│   └── imagens/              # Ícones do agente
├── SERVER/
│   └── Ver_0_B/             # Versão atual do servidor
│       ├── app.py           # Aplicação Flask principal
│       ├── config.py        # Configurações
│       ├── requirements.txt # Dependências completas
│       ├── requirements-minimal.txt # Dependências mínimas
│       ├── models/          # Modelos do banco de dados
│       ├── routes/          # Rotas da aplicação
│       ├── static/          # Arquivos estáticos (CSS, JS)
│       ├── templates/       # Templates HTML
│       └── modulos/         # Módulos específicos (PMOC)
└── venv_advansee/           # Ambiente virtual
```

## Dependências Principais

### Servidor (Flask)
- **Flask**: Framework web
- **Flask-SQLAlchemy**: ORM para banco de dados
- **psycopg2-binary**: Driver PostgreSQL
- **cryptography**: Criptografia para comunicação com agente
- **requests**: Requisições HTTP

### Agente
- **psutil**: Coleta de informações do sistema
- **wmi**: Gerenciamento Windows (apenas Windows)
- **pystray**: Interface de bandeja do sistema
- **Pillow**: Processamento de imagens
- **schedule**: Agendamento de tarefas
- **cryptography**: Criptografia para comunicação

## Troubleshooting

### Erro: "psycopg2 not found"
```bash
pip install psycopg2-binary
```

### Erro: "wmi module not found" (Windows)
```bash
pip install wmi pywin32
```

### Erro: "Permission denied" no PostgreSQL
Verifique se o usuário tem permissões no banco:
```sql
GRANT ALL PRIVILEGES ON DATABASE nome_do_banco TO usuario;
```

### Erro: "Port already in use"
Mude a porta no arquivo `app.py`:
```python
app.run(debug=True, port=5001)
```

### Erro: "Database connection failed"
Verifique as configurações em `config.py` e se o PostgreSQL está rodando.

## Desenvolvimento

### Instalar Dependências de Desenvolvimento
```bash
pip install -r requirements.txt
```

### Executar em Modo Debug
```bash
python app.py
```

### Logs
Os logs são salvos em: `~/logs/` (configurável em `config.py`)

## Produção

### Configurações de Produção
1. Desabilitar modo debug
2. Configurar servidor WSGI (Gunicorn, uWSGI)
3. Configurar proxy reverso (Nginx, Apache)
4. Configurar SSL/TLS
5. Configurar backup do banco de dados

### Exemplo com Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Suporte

Para dúvidas ou problemas:
1. Verifique os logs em `~/logs/`
2. Execute os scripts de teste
3. Verifique a documentação específica de cada módulo
4. Consulte o README do módulo PMOC se necessário 
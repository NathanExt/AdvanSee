# Resumo - Arquivos de Requirements e Instalação

## Arquivos Criados

### 1. Requirements do Servidor
- **`SERVER/Ver_0_B/requirements.txt`** - Dependências completas do servidor Flask
- **`SERVER/Ver_0_B/requirements-minimal.txt`** - Dependências mínimas essenciais

### 2. Requirements do Agente
- **`AGENTE/requirements.txt`** - Dependências específicas do agente

### 3. Scripts de Instalação
- **`install.bat`** - Script de instalação automatizada para Windows
- **`install.sh`** - Script de instalação automatizada para Linux/macOS

### 4. Documentação
- **`README_INSTALACAO.md`** - Guia completo de instalação e configuração

## Dependências Principais

### Servidor Flask
```
Flask==3.1.1
Flask-SQLAlchemy==3.1.1
psycopg2-binary==2.9.10
cryptography==45.0.5
requests==2.32.4
```

### Agente
```
cryptography==45.0.5
requests==2.32.4
psutil==6.1.0
Pillow==11.0.0
pystray==0.19.5
wmi==1.5.1 (Windows)
pywin32==306 (Windows)
schedule==1.2.1
```

## Como Usar

### Instalação Rápida (Windows)
```bash
# Execute o script de instalação
install.bat
```

### Instalação Rápida (Linux/macOS)
```bash
# Torne o script executável
chmod +x install.sh

# Execute o script de instalação
./install.sh
```

### Instalação Manual
```bash
# 1. Criar ambiente virtual
python -m venv venv_advansee

# 2. Ativar ambiente virtual
# Windows:
venv_advansee\Scripts\activate
# Linux/macOS:
source venv_advansee/bin/activate

# 3. Instalar dependências do servidor
cd SERVER/Ver_0_B
pip install -r requirements-minimal.txt

# 4. Instalar dependências do agente
cd ../../AGENTE
pip install -r requirements.txt
```

## Verificação da Instalação

### Testar Servidor
```bash
cd SERVER/Ver_0_B
python app.py
```

### Testar Agente
```bash
cd AGENTE
python agente.py
```

## Estrutura Final

```
AdvanSee/
├── install.bat                    # Script de instalação Windows
├── install.sh                     # Script de instalação Linux/macOS
├── README_INSTALACAO.md          # Guia de instalação
├── RESUMO_REQUIREMENTS.md        # Este arquivo
├── AGENTE/
│   ├── agente.py
│   ├── requirements.txt          # Dependências do agente
│   └── imagens/
├── SERVER/
│   └── Ver_0_B/
│       ├── app.py
│       ├── requirements.txt      # Dependências completas
│       ├── requirements-minimal.txt # Dependências mínimas
│       ├── models/
│       ├── routes/
│       ├── static/
│       ├── templates/
│       └── modulos/
└── venv_advansee/               # Ambiente virtual
```

## Benefícios

1. **Instalação Simplificada**: Scripts automatizados para diferentes sistemas
2. **Dependências Organizadas**: Separação clara entre servidor e agente
3. **Versões Fixas**: Evita problemas de compatibilidade
4. **Documentação Completa**: Guias detalhados de instalação
5. **Flexibilidade**: Opção de instalação mínima ou completa

## Próximos Passos

1. Execute o script de instalação apropriado para seu sistema
2. Configure o banco de dados PostgreSQL
3. Execute os scripts de migração
4. Inicie o servidor Flask
5. Teste o agente

## Suporte

Para problemas de instalação:
1. Verifique se o Python 3.8+ está instalado
2. Verifique se o PostgreSQL está configurado
3. Consulte o `README_INSTALACAO.md`
4. Execute os scripts de teste 
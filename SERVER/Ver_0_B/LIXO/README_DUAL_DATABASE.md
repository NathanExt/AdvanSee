# Sistema com Dois Bancos de Dados

## Visão Geral

O sistema foi reestruturado para suportar **dois bancos de dados independentes** de forma simples e organizada, mantendo a modularidade:

1. **Banco Principal (ISAC)**: `ISAC_BD_ADVANSEE_2`
2. **Banco PMOC**: `BD_PMOC`

## Arquitetura

### 📊 Banco Principal (ISAC)
- **Nome**: `ISAC_BD_ADVANSEE_2`
- **Propósito**: Sistema principal de inventário
- **Tabelas**: Organizations, Users, Assets, Categories, etc.
- **Instância SQLAlchemy**: `db`

### 💻 Banco PMOC
- **Nome**: `BD_PMOC`
- **Propósito**: Sistema de gerenciamento de equipamentos PMOC
- **Tabelas**: Notebook, Desktop
- **Instância SQLAlchemy**: `db_pmoc`

## Configuração

### Arquivo Principal (`config.py`)
```python
class CONFIG:
    # Configurações do banco principal (ISAC)
    DB_NAME_DEFAULT = "ISAC_BD_ADVANSEE_2"
    DATABASE_URL_DEFAULT = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_DEFAULT}"
    
    # Banco PMOC
    DB_NAME_PMOC = "BD_PMOC"
    DATABASE_URL_PMOC = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_PMOC}"
    
    # Configuração de múltiplos bancos
    SQLALCHEMY_BINDS = {
        'pmoc': DATABASE_URL_PMOC
    }
```

### Arquivo PMOC (`pmoc_config.py`)
```python
from config import CONFIG

class CONFIG_PMOC:
    # Usar configurações da classe principal
    DATABASE_URL_PMOC = CONFIG.DATABASE_URL_PMOC
```

## Estrutura dos Arquivos

### Backend
```
SERVER/Ver_0_B/
├── config.py                          # Configuração centralizada
├── app.py                             # Aplicação Flask principal
├── models/
│   └── database.py                    # Modelos do banco principal
└── modulos/pmoc/
    ├── pmoc_config.py                 # Configuração PMOC
    └── pmoc_models/
        └── pmoc_database.py           # Modelos do banco PMOC
```

### Modelos

#### Banco Principal (`models/database.py`)
```python
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Organization(db.Model):
    __tablename__ = 'organizations'
    # ... campos

class User(db.Model):
    __tablename__ = 'users'
    # ... campos
```

#### Banco PMOC (`modulos/pmoc/pmoc_models/pmoc_database.py`)
```python
from flask_sqlalchemy import SQLAlchemy
db_pmoc = SQLAlchemy()

class Notebook(db_pmoc.Model):
    __bind_key__ = 'pmoc'  # Especifica qual banco usar
    __tablename__ = 'notebook'
    # ... campos

class Desktop(db_pmoc.Model):
    __bind_key__ = 'pmoc'  # Especifica qual banco usar
    __tablename__ = 'desktop'
    # ... campos
```

## Configuração da Aplicação

### Inicialização (`app.py`)
```python
# Configuração dos bancos de dados
app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG.DATABASE_URL_DEFAULT
app.config['SQLALCHEMY_BINDS'] = CONFIG.SQLALCHEMY_BINDS

# Inicializar bancos de dados
db.init_app(app)        # Banco principal
db_pmoc.init_app(app)   # Banco PMOC

def create_tables():
    """Criar tabelas em ambos os bancos de dados"""
    with app.app_context():
        db.create_all()      # Criar tabelas do banco principal
        db_pmoc.create_all() # Criar tabelas do banco PMOC
```

## Como Usar

### 1. Consultas no Banco Principal
```python
from models.database import db, Organization, User, Asset

# Consultas normais (usam o banco principal)
organizations = Organization.query.all()
users = User.query.filter_by(is_active=True).all()
```

### 2. Consultas no Banco PMOC
```python
from modulos.pmoc.pmoc_models.pmoc_database import db_pmoc, Notebook, Desktop

# Consultas no banco PMOC
notebooks = Notebook.query.all()
desktops = Desktop.query.filter_by(status='Em uso').all()
```

### 3. Transações
```python
# Banco principal
with db.session.begin():
    new_org = Organization(name="Nova Org")
    db.session.add(new_org)

# Banco PMOC
with db_pmoc.session.begin():
    new_notebook = Notebook(id="123", model="ThinkPad")
    db_pmoc.session.add(new_notebook)
```

## Vantagens da Nova Estrutura

### ✅ **Modularidade**
- Cada módulo tem seu próprio banco
- Configuração centralizada
- Fácil manutenção

### ✅ **Simplicidade**
- Configuração única em `config.py`
- Herança de configurações
- Código limpo e organizado

### ✅ **Flexibilidade**
- Fácil adicionar novos bancos
- Configuração independente por banco
- Migrações separadas

### ✅ **Performance**
- Queries otimizadas por banco
- Conexões independentes
- Sem conflitos de schema

## Testes

### Script de Teste
```bash
python test_dual_database.py
```

### O que o teste verifica:
1. ✅ Configuração correta
2. ✅ URLs dos bancos diferentes
3. ✅ Conexão com ambos os bancos
4. ✅ Consultas funcionando
5. ✅ Contagem de registros

## Troubleshooting

### Problemas Comuns

#### 1. Erro de Bind Key
```
Error: No bind key 'pmoc' found
```
**Solução**: Verificar se `SQLALCHEMY_BINDS` está configurado corretamente

#### 2. Erro de Conexão
```
Error: connection to server failed
```
**Solução**: Verificar se os bancos existem e as credenciais estão corretas

#### 3. Tabelas não encontradas
```
Error: relation "notebook" does not exist
```
**Solução**: Executar `create_tables()` para criar as tabelas

#### 4. Configuração duplicada
```
Error: multiple database configurations
```
**Solução**: Usar apenas uma configuração centralizada

### Logs Úteis
- **Flask**: `app.logger.info("Mensagem")`
- **SQLAlchemy**: `echo=True` na configuração
- **PostgreSQL**: Logs de conexão e queries

## Próximos Passos

### Melhorias Planejadas
- [ ] Migrações automáticas
- [ ] Backup automático
- [ ] Monitoramento de performance
- [ ] Cache distribuído
- [ ] Replicação de dados

### Novos Módulos
- [ ] Sistema de auditoria
- [ ] Relatórios cross-database
- [ ] Sincronização de dados
- [ ] API REST unificada

## Suporte

Para dúvidas ou problemas:
1. Verificar este README
2. Executar o script de teste
3. Verificar logs do sistema
4. Consultar documentação do SQLAlchemy 
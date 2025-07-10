# Módulo PMOC com SQLAlchemy

## Mudanças Implementadas

### 1. Arquivo `pmoc_database.py`

O arquivo foi completamente refatorado para usar **Flask-SQLAlchemy** da mesma forma que o arquivo `database.py` principal:

#### Antes:
```python
from sqlalchemy import Column, String, Date, Text, Numeric, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

db_pmoc = SQLAlchemy()
Base = declarative_base()

class Notebook(Base):
    __tablename__ = 'notebook'
    # ... campos usando Column()
```

#### Depois:
```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Usar a mesma instância do SQLAlchemy do projeto principal
from models.database import db

class Notebook(db.Model):
    __tablename__ = 'notebook'
    # ... campos usando db.Column()
```

### 2. Arquivo `pmoc_main.py`

#### Principais mudanças:

1. **Importação atualizada**: Agora importa `Notebook, Desktop` diretamente do novo modelo
2. **Criação de objetos**: Mudou de construtor com parâmetros nomeados para atribuição de atributos
3. **Criação de tabelas**: Usa SQL direto para criar tabelas quando necessário

#### Exemplo de criação de objeto:

```python
# Antes:
return Notebook(
    id=data.get("id", ""),
    model=data.get("model", ""),
    # ...
)

# Depois:
notebook = Notebook()
notebook.id = data.get("id", "")
notebook.model = data.get("model", "")
# ...
return notebook
```

### 3. Configuração do Banco

O banco foi alterado para `BD_PMOC` conforme solicitado no arquivo `pmoc_config.py`.

## Como Usar

### 1. Executar o Teste

```bash
cd SERVER/Ver_0_B/modulos/pmoc
python test_pmoc_sqlalchemy.py
```

### 2. Usar no Código Principal

```python
from modulos.pmoc.pmoc_main import PMOC

# Instanciar o módulo
pmoc = PMOC()

# Criar tabelas (se necessário)
pmoc.create_pmoc_tables()

# Gravar dados
pmoc.grava_dados_notebook()
pmoc.grava_dados_desktop()
```

## Vantagens da Mudança

1. **Consistência**: Agora usa a mesma estrutura do projeto principal
2. **Manutenibilidade**: Código mais limpo e padronizado
3. **Integração**: Melhor integração com Flask-SQLAlchemy
4. **Compatibilidade**: Funciona com o sistema de migrações do Flask-SQLAlchemy

## Estrutura das Tabelas

### Tabela `notebook`
- `id` (VARCHAR(255), PRIMARY KEY)
- `model` (TEXT)
- `patrimony` (VARCHAR(255))
- `manufacturer` (TEXT)
- `equipment_value` (NUMERIC(10, 2))
- `tag_uisa` (VARCHAR(255))
- `created_at` (DATE)
- `updated_by` (VARCHAR(255))
- `tag` (VARCHAR(255))
- `os_version` (TEXT)
- `entry_note` (VARCHAR(255))
- `status` (VARCHAR(255))
- `date_home` (DATE)
- `date_end` (DATE)
- `updated_at` (TIMESTAMP)
- `rc` (VARCHAR(255))
- `owner` (VARCHAR(255))
- `processor` (TEXT)
- `type` (VARCHAR(255))
- `ram_memory` (VARCHAR(255))
- `last_inventory_date` (DATE)
- `contract_type` (VARCHAR(255))
- `os_architecture` (VARCHAR(255))

### Tabela `desktop`
- Mesma estrutura da tabela `notebook`

## Troubleshooting

### Erro de Conexão
- Verificar se o PostgreSQL está rodando
- Verificar se o banco `BD_PMOC` existe
- Verificar credenciais no `pmoc_config.py`

### Erro de Tabela Não Encontrada
- Executar `pmoc.create_pmoc_tables()` primeiro
- Verificar permissões do usuário no banco

### Erro de Importação
- Verificar se o path está correto
- Verificar se todos os arquivos estão no lugar certo 
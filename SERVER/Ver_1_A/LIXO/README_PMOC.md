# Módulo PMOC - Solução para Erro de Gravação

## Problema Identificado

O erro `psycopg2.OperationalError` ocorre porque a **tabela `notebook` não existe no banco de dados `DB_PMOC`**.

## Solução

### Passo 1: Criar a Tabela no Banco de Dados

Execute um dos seguintes métodos:

#### Opção A: Script Python (Recomendado)
```bash
cd SERVER/Ver_0_B/modulos/pmoc
python create_pmoc_tables.py
```

#### Opção B: Script SQL Manual
1. Conecte ao PostgreSQL:
```bash
psql -h 127.0.0.1 -U isac -d DB_PMOC
```

2. Execute o script SQL:
```sql
\i create_notebook_table.sql
```

### Passo 2: Verificar se Tudo Está Funcionando

Execute o script de teste:
```bash
cd SERVER/Ver_0_B/modulos/pmoc
python test_pmoc.py
```

### Passo 3: Executar a Gravação dos Dados

Após criar a tabela, você pode executar a gravação dos dados:

```python
from modulos.pmoc.pmoc_main import PMOC

pmoc = PMOC()
pmoc.grava_dados()
```

## Estrutura da Tabela

A tabela `notebook` possui os seguintes campos:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | VARCHAR | ID único do notebook |
| model | TEXT | Modelo do equipamento |
| patrimony | VARCHAR | Número do patrimônio |
| manufacturer | TEXT | Fabricante |
| equipment_value | NUMERIC(10,2) | Valor do equipamento |
| tag_uisa | VARCHAR | Tag UISA |
| created_at | DATE | Data de criação |
| updated_by | VARCHAR | Usuário que atualizou |
| tag | VARCHAR | Tag do equipamento |
| os_version | TEXT | Versão do sistema operacional |
| entry_note | VARCHAR | Nota de entrada |
| status | VARCHAR | Status do equipamento |
| date_home | DATE | Data de chegada |
| date_end | DATE | Data de fim |
| updated_at | TIMESTAMP | Data de atualização |
| rc | VARCHAR | RC |
| owner | VARCHAR | Proprietário |
| processor | TEXT | Processador |
| type | VARCHAR | Tipo |
| ram_memory | VARCHAR | Memória RAM |
| last_inventory_date | DATE | Data do último inventário |
| contract_type | VARCHAR | Tipo de contrato |
| os_architecture | VARCHAR | Arquitetura do SO |

## Configuração do Banco

O módulo PMOC usa um banco de dados separado (`DB_PMOC`) com as seguintes configurações:

- **Host**: 127.0.0.1
- **Porta**: 5432
- **Banco**: DB_PMOC
- **Usuário**: isac
- **Senha**: kwa44fgjc8suf91kjsacaz

## Verificações Importantes

1. **Banco de Dados Existe**: Certifique-se de que o banco `DB_PMOC` foi criado
2. **Usuário Tem Permissões**: O usuário `isac` deve ter permissões de CREATE, INSERT, UPDATE, DELETE
3. **PostgreSQL Rodando**: O serviço PostgreSQL deve estar ativo
4. **Conexão de Rede**: Verifique se consegue conectar ao PostgreSQL

## Troubleshooting

### Erro: "database does not exist"
```sql
CREATE DATABASE DB_PMOC;
```

### Erro: "permission denied"
```sql
GRANT ALL PRIVILEGES ON DATABASE DB_PMOC TO isac;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO isac;
```

### Erro: "connection refused"
- Verifique se o PostgreSQL está rodando
- Verifique se a porta 5432 está acessível
- Verifique as configurações de firewall

## Logs e Debug

Para habilitar logs detalhados, adicione no código:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contato

Em caso de problemas, verifique:
1. Os logs de erro
2. A conectividade com o banco
3. As permissões do usuário
4. A existência da tabela 
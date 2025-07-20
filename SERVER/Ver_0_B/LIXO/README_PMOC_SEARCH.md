# Implementação da Busca no Banco PMOC

## Solicitação

Utilizar a Tag e o patrimônio para buscar assets que estejam registrados no banco de dados DB_PMOC, utilizando o hostname da máquina como patrimônio (onde NBKMT001069 é o hostname e 001069 é o patrimônio), realizando uma busca dupla utilizando o patrimônio e a tag do asset no banco de dados PMOC.

## Arquitetura da Solução

### 1. Módulo de Busca PMOC (`pmoc_search.py`)

**Localização:** `SERVER/Ver_0_B/modulos/pmoc/pmoc_search.py`

**Funcionalidades:**
- Extração automática de patrimônio do hostname
- Busca dupla por tag e patrimônio
- Conexão com banco DB_PMOC
- Suporte a notebooks e desktops

#### Classe Principal: `PMOCSearch`

```python
class PMOCSearch:
    def __init__(self):
        """Inicializa conexão com banco PMOC"""
        
    def extract_patrimony_from_hostname(self, hostname):
        """Extrai patrimônio do hostname (ex: NBKMT001069 -> 001069)"""
        
    def search_by_tag_and_patrimony(self, tag, patrimony):
        """Busca dupla no banco PMOC usando tag e patrimônio"""
        
    def search_asset_by_hostname_and_tag(self, hostname, tag):
        """Busca asset usando hostname e tag"""
        
    def get_asset_details(self, asset_id, asset_type):
        """Busca detalhes completos de um asset específico"""
```

#### Extração de Patrimônio

**Algoritmo:**
1. Busca por 6 dígitos consecutivos no final do hostname
2. Fallback para qualquer sequência de dígitos
3. Preenchimento com zeros à esquerda se necessário

**Exemplos:**
- `NBKMT001069` → `001069`
- `DESKTOP123456` → `123456`
- `PC-001234` → `001234`

#### Busca Dupla

**Estratégia:**
```python
# Busca OR para maximizar resultados
WHERE tag = :tag OR tag_uisa = :tag OR patrimony = :patrimony
```

**Tabelas pesquisadas:**
- `notebook` (tabela de notebooks)
- `desktop` (tabela de desktops)

### 2. Integração com Checkin de Agentes

**Localização:** `SERVER/Ver_0_B/routes/rotas_agente/rt_agente_checkin.py`

**Funcionalidade:**
- Busca automática no PMOC durante o checkin
- Registro no histórico do asset
- Não interrompe o checkin em caso de erro

```python
# Buscar informações complementares no banco PMOC
try:
    hostname = asset.name if asset.name else asset.asset_tag
    tag = asset.tag if asset.tag else None
    
    if hostname or tag:
        pmoc_results = search_pmoc_asset(hostname, tag)
        
        if pmoc_results and 'error' not in pmoc_results and pmoc_results.get('total_found', 0) > 0:
            # Adicionar informações no histórico
            history = AssetHistory(
                asset_id=asset.id,
                user_id=None,
                action='pmoc_info_found',
                new_value=f"Informações PMOC encontradas: {pmoc_info}"
            )
            db.session.add(history)
            
except Exception as pmoc_error:
    print(f"Erro ao buscar no PMOC: {pmoc_error}")
    # Não falha o checkin
```

### 3. Visualização em Asset Details

**Localização:** `SERVER/Ver_0_B/routes/rotas_site/rt_asset_detail.py`

**Funcionalidade:**
- Busca PMOC automática ao visualizar asset
- Seção dedicada no template
- Link para busca detalhada

**Modificações na função `dados_asset()`:**
```python
# Buscar informações no PMOC
pmoc_info = None
try:
    hostname = asset.name if asset.name else asset.asset_tag
    tag = asset.tag if asset.tag else None
    
    if hostname or tag:
        pmoc_results = search_pmoc_asset(hostname, tag)
        if pmoc_results and 'error' not in pmoc_results and pmoc_results.get('total_found', 0) > 0:
            pmoc_info = pmoc_results
except Exception as e:
    print(f"Erro ao buscar informações PMOC: {e}")
    pmoc_info = None
```

### 4. Interface Web para Testes

**Localização:** `SERVER/Ver_0_B/routes/rotas_site/rt_pmoc_search.py`

**Rotas disponíveis:**
- `/pmoc/search` - Página de busca
- `/pmoc/search/api` - API de busca
- `/pmoc/asset/<type>/<id>` - Detalhes de asset
- `/pmoc/test/patrimony` - Teste de extração

**Template:** `SERVER/Ver_0_B/templates/pmoc_search.html`

## Estrutura dos Dados

### Tabela `notebook` (DB_PMOC)

```sql
CREATE TABLE notebook (
    id VARCHAR(255) PRIMARY KEY,
    model TEXT,
    patrimony VARCHAR(255),
    manufacturer TEXT,
    tag VARCHAR(255),
    tag_uisa VARCHAR(255),
    status VARCHAR(255),
    owner VARCHAR(255),
    processor TEXT,
    ram_memory VARCHAR(255),
    os_version TEXT,
    contract_type VARCHAR(255),
    -- outros campos...
);
```

### Tabela `desktop` (DB_PMOC)

```sql
CREATE TABLE desktop (
    id VARCHAR(255) PRIMARY KEY,
    model TEXT,
    patrimony VARCHAR(255),
    manufacturer TEXT,
    tag VARCHAR(255),
    tag_uisa VARCHAR(255),
    status VARCHAR(255),
    owner VARCHAR(255),
    processor TEXT,
    ram_memory VARCHAR(255),
    os_version TEXT,
    contract_type VARCHAR(255),
    -- outros campos...
);
```

### Formato de Resposta

```json
{
    "notebooks": [
        {
            "id": "NOTEBOOK_001",
            "model": "ThinkPad X1 Carbon",
            "patrimony": "001069",
            "manufacturer": "Lenovo",
            "tag": "UISA_TAG",
            "tag_uisa": "UISA_001069",
            "status": "ativo",
            "owner": "João Silva",
            "type": "notebook"
        }
    ],
    "desktops": [],
    "total_found": 1,
    "extracted_patrimony": "001069",
    "search_params": {
        "hostname": "NBKMT001069",
        "tag": "UISA_TAG",
        "patrimony_extracted": "001069"
    }
}
```

## Casos de Uso

### 1. Checkin de Agente

**Cenário:** Agente NBKMT001069 faz checkin com tag "UISA_TAG_001"

**Processo:**
1. Agente envia dados do sistema
2. Sistema extrai patrimônio: `001069`
3. Busca no PMOC: `tag = 'UISA_TAG_001' OR patrimony = '001069'`
4. Registra resultado no histórico do asset
5. Continua processo de checkin normalmente

### 2. Visualização de Asset

**Cenário:** Usuário visualiza detalhes do asset

**Processo:**
1. Usuário acessa `/asset/123`
2. Sistema busca automaticamente no PMOC
3. Exibe seção "Informações do PMOC"
4. Mostra dados encontrados ou mensagem de "não encontrado"

### 3. Busca Manual

**Cenário:** Usuário quer buscar manualmente no PMOC

**Processo:**
1. Usuário acessa `/pmoc/search`
2. Insere hostname e/ou tag
3. Sistema realiza busca e exibe resultados
4. Usuário pode ver detalhes completos

## Instalação e Configuração

### 1. Dependências

```bash
pip install sqlalchemy psycopg2-binary
```

### 2. Configuração do Banco

**Arquivo:** `SERVER/Ver_0_B/config.py`

```python
# Banco PMOC
DB_NAME_PMOC = "DB_PMOC"
DATABASE_URL_PMOC = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_PMOC}"

# Configuração de múltiplos bancos
SQLALCHEMY_BINDS = {
    'pmoc': DATABASE_URL_PMOC
}
```

### 3. Registro de Blueprints

**Arquivo:** `SERVER/Ver_0_B/app.py`

```python
from routes.rotas_site import rt_pmoc_search
app.register_blueprint(rt_pmoc_search.bp_pmoc_search)
```

## Testes

### 1. Teste de Extração de Patrimônio

**URL:** `/pmoc/test/patrimony`

**Casos testados:**
- NBKMT001069 → 001069
- DESKTOP123456 → 123456
- PC-001234 → 001234
- INVALID-HOST → null

### 2. Teste de Busca Manual

**URL:** `/pmoc/search`

**Cenários:**
- Busca por hostname apenas
- Busca por tag apenas
- Busca por ambos
- Busca sem resultados

### 3. Teste de Integração

**Script:** `SERVER/Ver_0_B/test_pmoc_integration.py`

```python
from modulos.pmoc.pmoc_search import search_pmoc_asset

# Teste básico
result = search_pmoc_asset('NBKMT001069', 'UISA_TAG')
print(f"Resultados: {result}")

# Teste de extração
from modulos.pmoc.pmoc_search import PMOCSearch
searcher = PMOCSearch()
patrimony = searcher.extract_patrimony_from_hostname('NBKMT001069')
print(f"Patrimônio extraído: {patrimony}")
```

## Logs e Monitoramento

### 1. Logs de Checkin

```
Buscando no PMOC - Hostname: NBKMT001069, Tag: UISA_TAG, Patrimônio extraído: 001069
Informações PMOC adicionadas ao histórico do asset 1
```

### 2. Logs de Erro

```
Erro ao buscar no PMOC: connection timeout
Erro ao buscar informações PMOC para asset 123: database connection failed
```

### 3. Histórico de Assets

**Tabela:** `asset_history`

```sql
SELECT * FROM asset_history 
WHERE action = 'pmoc_info_found' 
ORDER BY timestamp DESC;
```

## Tratamento de Erros

### 1. Conexão com Banco

**Problema:** Falha na conexão com DB_PMOC
**Solução:** Não interrompe o checkin, registra log de erro

### 2. Asset Não Encontrado

**Problema:** Nenhum asset encontrado no PMOC
**Solução:** Exibe mensagem informativa, não é considerado erro

### 3. Dados Inválidos

**Problema:** Hostname não contém patrimônio válido
**Solução:** Continua busca apenas por tag

## Performance

### 1. Otimizações

- Conexão reutilizada durante busca
- Índices nas colunas `patrimony`, `tag`, `tag_uisa`
- Timeout configurável para evitar travamentos

### 2. Cache (Futuro)

```python
# Implementação futura de cache
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@cache.memoize(timeout=300)
def search_pmoc_asset_cached(hostname, tag):
    return search_pmoc_asset(hostname, tag)
```

## Segurança

### 1. Sanitização de Entrada

```python
def sanitize_input(text):
    if not text:
        return None
    return re.sub(r'[^\w\-_.]', '', text)[:255]
```

### 2. Permissões

- Busca PMOC não requer autenticação adicional
- Usa mesmas credenciais do banco principal
- Acesso read-only ao banco PMOC

## Conclusão

A implementação da busca no banco PMOC foi realizada com sucesso, oferecendo:

- **Busca dupla automática** por tag e patrimônio
- **Integração transparente** com checkin de agentes
- **Interface web** para testes e buscas manuais
- **Visualização integrada** nos detalhes do asset
- **Tratamento robusto de erros**
- **Performance otimizada**

A solução permite correlacionar automaticamente assets do sistema principal com registros do banco PMOC, enriquecendo as informações disponíveis e facilitando a gestão de ativos. 
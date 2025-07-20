# Sincronização PMOC - AdvanSee

## Visão Geral

Este módulo permite sincronizar os dados dos equipamentos encontrados no PMOC (Sistema de Patrimônio) com o banco de dados local do AdvanSee. A sincronização cria uma tabela `pmoc_assets` que armazena os dados dos equipamentos encontrados no PMOC e os relaciona com os assets locais.

## Funcionalidades

- **Sincronização Automática**: Busca dados de notebooks e desktops no PMOC via API
- **Matching Inteligente**: Relaciona equipamentos do PMOC com assets locais usando tags, tags UISA e números de patrimônio
- **Interface Web**: Botão na página de assets para executar a sincronização
- **Estatísticas Detalhadas**: Mostra resultados da sincronização com contadores
- **Histórico de Sincronização**: Mantém registro da última sincronização

## Estrutura da Tabela

A tabela `pmoc_assets` contém os seguintes campos:

- `id`: Chave primária
- `asset_id`: Referência ao asset local
- `pmoc_type`: Tipo do equipamento ('notebook' ou 'desktop')
- `pmoc_id`: ID do equipamento no PMOC
- `tag`: Tag do equipamento no PMOC
- `tag_uisa`: Tag UISA do equipamento
- `patrimony`: Número do patrimônio
- `manufacturer`: Fabricante
- `model`: Modelo
- `serial_number`: Número de série
- `user_name`: Nome do usuário
- `department`: Departamento
- `location`: Localização
- `status`: Status no PMOC
- `last_sync`: Data/hora da última sincronização
- `created_at`: Data de criação do registro
- `updated_at`: Data da última atualização

## Instalação

### 1. Criar a Tabela no Banco de Dados

Execute o script SQL para criar a tabela:

```sql
-- Execute o arquivo create_pmoc_assets_table.sql no seu banco PostgreSQL
```

### 2. Verificar Dependências

Certifique-se de que as seguintes dependências estão instaladas:

```bash
pip install requests flask-sqlalchemy
```

### 3. Configurar API do PMOC

Verifique se as URLs da API do PMOC estão corretas no arquivo `modulos/pmoc/pmoc_assets.py`:

```python
# URL para notebooks
url = 'https://sensedia.uisa.com.br/app-equipment/api/v1/firebase/get?environment=prd&type=notebook'

# URL para desktops
url = 'https://sensedia.uisa.com.br/app-equipment/api/v1/firebase/get?environment=prd&type=desktop'
```

## Como Usar

### Via Interface Web

1. Acesse a página de Assets (`/assets`)
2. Escolha entre dois métodos de sincronização:
   - **Sincronizar PMOC (API)**: Usa a API do PMOC para buscar dados
   - **Sincronizar PMOC (Banco)**: Busca direta no banco de dados PMOC (recomendado)
3. Clique no botão desejado
4. Aguarde a conclusão da sincronização
5. Visualize as estatísticas de resultados

### Via API

```bash
# Versão 1 (API)
curl -X POST http://localhost:5000/assets/sync-pmoc

# Versão 2 (Banco direto)
curl -X POST http://localhost:5000/assets/sync-pmoc-v2
```

### Via Código Python

```python
# Versão 1 (API)
from modulos.pmoc.pmoc_assets import sync_pmoc_assets
stats = sync_pmoc_assets()

# Versão 2 (Banco direto)
from modulos.pmoc.pmoc_assets import sync_pmoc_assets_2
stats = sync_pmoc_assets_2()

# Verificar resultados (versão 2)
print(f"Assets processados: {stats['assets_processed']}")
print(f"Assets encontrados: {stats['assets_matched']}")
print(f"Registros criados: {stats['assets_created']}")
print(f"Registros atualizados: {stats['assets_updated']}")
```

## Versões de Sincronização

### Versão 1 (API)
- **Método**: Usa a API REST do PMOC
- **Vantagens**: Não requer acesso direto ao banco PMOC
- **Desvantagens**: Dependente da disponibilidade da API
- **Endpoint**: `/assets/sync-pmoc`

### Versão 2 (Banco Direto) - **Recomendada**
- **Método**: Conexão direta ao banco de dados PMOC
- **Vantagens**: Mais rápida, mais confiável, busca mais precisa
- **Desvantagens**: Requer acesso direto ao banco PMOC
- **Endpoint**: `/assets/sync-pmoc-v2`

## Algoritmo de Matching

### Versão 1 (API)
O sistema utiliza a seguinte lógica para relacionar equipamentos do PMOC com assets locais:

1. **Busca por Tag**: Procura assets com `tag` ou `asset_tag` igual ao `tag` do PMOC
2. **Busca por Tag UISA**: Procura assets com `tag` ou `asset_tag` igual ao `tag_uisa` do PMOC
3. **Busca por Patrimônio**: Procura assets com `name` igual ao `patrimony` do PMOC

### Versão 2 (Banco Direto)
Utiliza a classe `PMOCSearch` que implementa:

1. **Extração de Patrimônio**: Extrai números de patrimônio do hostname
2. **Busca Multi-campo**: Busca por TAG, TAG_UISA e PATRIMÔNIO simultaneamente
3. **Matching Inteligente**: Combina resultados de notebooks e desktops
4. **Limpeza de Dados**: Remove espaços e normaliza strings

## Estatísticas Disponíveis

Após a sincronização, as seguintes estatísticas são exibidas:

- **Notebooks processados**: Quantidade de notebooks encontrados no PMOC
- **Desktops processados**: Quantidade de desktops encontrados no PMOC
- **Assets encontrados**: Quantidade de assets locais que foram relacionados
- **Registros criados**: Novos registros na tabela `pmoc_assets`
- **Registros atualizados**: Registros existentes que foram atualizados
- **Erros**: Lista de erros encontrados durante a sincronização

## Monitoramento

### Verificar Última Sincronização

```sql
SELECT 
    asset_id,
    pmoc_type,
    pmoc_id,
    tag,
    user_name,
    department,
    last_sync
FROM pmoc_assets 
ORDER BY last_sync DESC;
```

### Verificar Assets sem Correspondência no PMOC

```sql
SELECT 
    a.id,
    a.name,
    a.asset_tag,
    a.tag
FROM assets a
LEFT JOIN pmoc_assets pa ON a.id = pa.asset_id
WHERE pa.asset_id IS NULL;
```

## Troubleshooting

### Erro de Conexão com API

- Verifique se as URLs da API estão corretas
- Confirme se o servidor tem acesso à internet
- Verifique se há firewall bloqueando as requisições

### Erro de Banco de Dados

- Execute o script SQL para criar a tabela
- Verifique se as permissões de banco estão corretas
- Confirme se o modelo `PmocAsset` está importado corretamente

### Assets não Encontrados

- Verifique se os campos `tag`, `asset_tag` e `name` dos assets estão preenchidos
- Confirme se os dados do PMOC estão corretos
- Ajuste o algoritmo de matching se necessário

## Logs

Os logs de sincronização são exibidos na interface web e também podem ser encontrados nos logs da aplicação Flask.

## Testes

### Script de Teste Automatizado

Execute o script de teste para verificar se a sincronização está funcionando:

```bash
cd SERVER/Ver_0_B
python test_sync_pmoc_v2.py
```

O script irá:
- Testar a busca de um asset individual
- Executar a sincronização completa
- Exibir estatísticas detalhadas
- Mostrar exemplos de registros criados

### Teste Manual

1. Execute a sincronização via interface web
2. Verifique os logs no console da aplicação
3. Consulte a tabela `pmoc_assets` para verificar os registros criados
4. Verifique a coluna "PMOC" na tabela de assets

## Troubleshooting

### Erro de Conexão com Banco PMOC

- Verifique se as configurações em `modulos/pmoc/pmoc_config.py` estão corretas
- Confirme se o servidor tem acesso ao banco PMOC
- Teste a conexão usando o script de teste

### Assets não Encontrados

- Verifique se os campos `tag`, `asset_tag` e `name` dos assets estão preenchidos
- Confirme se os dados do PMOC estão corretos
- Use a versão 2 (banco direto) para busca mais precisa

### Erro de Banco de Dados

- Execute o script SQL para criar a tabela
- Verifique se as permissões de banco estão corretas
- Confirme se o modelo `PmocAsset` está importado corretamente

## Contribuição

Para adicionar novos campos ou funcionalidades:

1. Atualize o modelo `PmocAsset` em `models/database.py`
2. Modifique a função `_process_pmoc_item` em `modulos/pmoc/pmoc_assets.py`
3. Atualize o script SQL se necessário
4. Teste a funcionalidade antes de fazer deploy
5. Execute o script de teste para validar as mudanças 
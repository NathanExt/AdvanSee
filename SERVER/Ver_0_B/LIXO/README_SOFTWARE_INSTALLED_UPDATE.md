# Atualização: Dados da Página Software baseados em installed_software

## Alteração Realizada

A página `software.html` foi modificada para utilizar dados da tabela `installed_software` ao invés da tabela `software` como fonte principal das informações.

## Mudanças Implementadas

### 1. Fonte de Dados Principal
- **Antes**: Tabela `software` (produtos de software cadastrados)
- **Depois**: Tabela `installed_software` (software realmente instalado nos assets)

### 2. Arquivos Modificados

#### `routes/rotas_site/rt_software.py`
- Query principal alterada de `Software.query` para `InstalledSoftware.query`
- Filtros de busca adaptados para usar `InstalledSoftware.name` e `InstalledSoftware.vendor`
- API de busca modificada para retornar dados de `installed_software`
- Gráfico de "Distribuição de Licenças" substituído por "Distribuição por Fabricante"

#### `templates/software.html`
- Tabela atualizada para mostrar colunas relevantes da tabela `installed_software`:
  - **ID**: ID do registro de software instalado
  - **Nome**: Nome do software
  - **Fabricante**: Fabricante do software
  - **Versão**: Versão instalada
  - **Asset ID**: ID do asset onde está instalado (nova coluna)
  - **Data de Criação**: Data do registro
- Título da tabela alterado para "Lista de Software Instalado"
- Gráfico renomeado para "Distribuição por Fabricante"

#### `static/js/software.js`
- Função de busca dinâmica adaptada para trabalhar com `asset_id`
- Gráfico de distribuição atualizado para mostrar fabricantes ao invés de licenças
- Contador de resultados atualizado para "Software Instalado"

### 3. Estrutura da Tabela installed_software

A tabela `installed_software` contém:
```sql
CREATE TABLE installed_software (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    version VARCHAR(100),
    vendor VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(asset_id, name, version, vendor)
);
```

### 4. Vantagens da Mudança

1. **Dados Reais**: Mostra software realmente instalado nos equipamentos
2. **Rastreabilidade**: Cada entrada está associada a um asset específico
3. **Inventário Atual**: Reflete o que está realmente sendo usado na organização
4. **Relatórios Precisos**: Gráficos baseados em dados de instalação real

### 5. Estatísticas Atualizadas

- **Produtos de Software**: Mantém contagem da tabela `software` (produtos cadastrados)
- **Software Instalado**: Total de instalações na tabela `installed_software`
- **Software Único**: Número de tipos únicos de software instalado

### 6. Gráficos Atualizados

1. **Top 10 Software Mais Instalados**: Baseado em `installed_software`
2. **Top 10 Fabricantes**: Baseado em `installed_software`
3. **Distribuição por Fabricante**: Substitui o gráfico de licenças, mostra distribuição de fabricantes

### 7. Funcionalidades de Busca

- **Busca por Nome**: Filtra por nome do software instalado
- **Busca por Fabricante**: Filtra por fabricante do software instalado
- **Busca Dinâmica**: Atualização em tempo real via AJAX
- **Asset ID**: Permite identificar em qual equipamento está instalado

## Impacto da Mudança

### Positivo
- Dados mais precisos e atuais
- Melhor rastreabilidade por asset
- Inventário baseado em dados reais de campo
- Possibilidade de análises por equipamento

### Considerações
- Os dados da tabela `software` (produtos cadastrados) ainda são mantidos para referência
- A estatística "Produtos de Software" ainda reflete a tabela `software` original
- Possibilidade futura de criar uma view combinada das duas tabelas se necessário

## Próximos Passos Sugeridos

1. **Link para Assets**: Adicionar link do Asset ID para a página de detalhes do asset
2. **Filtro por Asset**: Permitir filtrar software por asset específico
3. **Relatórios**: Criar relatórios de software por departamento/localização
4. **Comparação**: View que compare software cadastrado vs instalado
5. **Alertas**: Notificações para software não licenciado ou versões desatualizadas

A página agora reflete com maior precisão o inventário real de software da organização! 
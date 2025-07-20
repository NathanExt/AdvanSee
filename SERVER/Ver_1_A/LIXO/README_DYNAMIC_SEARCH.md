# Busca Dinâmica de Assets - AdvanSee

## Visão Geral

A funcionalidade de busca dinâmica permite pesquisar assets em tempo real, sem necessidade de recarregar a página. A busca é similar à implementada na página PMOC, oferecendo uma experiência de usuário mais fluida e responsiva.

## Funcionalidades

- **Busca em Tempo Real**: Resultados atualizados instantaneamente
- **Múltiplos Filtros**: Nome/Tag, Fabricante, Modelo, Usuário, Status
- **Busca Automática**: Ativa após parar de digitar (debounce)
- **Loading State**: Indicador visual durante a busca
- **Contador Dinâmico**: Número de resultados atualizado automaticamente
- **Status PMOC**: Indica se o asset está sincronizado com PMOC

## Como Funciona

### Interface do Usuário

1. **Campos de Busca**:
   - **Nome/Tag**: Busca por nome do asset ou asset tag
   - **Fabricante**: Filtro por fabricante do equipamento
   - **Modelo**: Filtro por modelo do equipamento
   - **Usuário**: Busca por usuário logado
   - **Status**: Filtro por status do asset

2. **Botões**:
   - **Buscar**: Executa a busca manualmente
   - **Limpar**: Remove todos os filtros e recarrega dados

### Comportamento da Busca

#### Busca Automática
- **Campos de texto**: Busca automática após 500ms de inatividade
- **Campos select**: Busca imediata ao alterar seleção
- **Debounce**: Evita múltiplas requisições durante digitação

#### Busca Manual
- Clique no botão "Buscar" para executar busca imediata
- Útil quando há muitos filtros ativos

## Implementação Técnica

### Frontend (JavaScript)

```javascript
// Função principal de busca
function performSearch() {
    const searchParams = {
        search_name: document.getElementById('search_name').value,
        search_manufacturer: document.getElementById('search_manufacturer').value,
        search_model: document.getElementById('search_model').value,
        search_user: document.getElementById('search_user').value,
        search_status: document.getElementById('search_status').value
    };
    
    // Construir query string
    const queryString = Object.keys(searchParams)
        .filter(key => searchParams[key])
        .map(key => `${key}=${encodeURIComponent(searchParams[key])}`)
        .join('&');
    
    fetch(`/assets/api/search?${queryString}`)
        .then(response => response.json())
        .then(data => {
            displaySearchResults(data);
        });
}
```

### Backend (Python/Flask)

```python
@bp_assets.route('/assets/api/search')
def assets_api_search():
    """API endpoint para busca de assets via AJAX"""
    # Obter parâmetros de busca
    search_name = request.args.get('search_name', '')
    search_manufacturer = request.args.get('search_manufacturer', '')
    # ... outros parâmetros
    
    # Aplicar filtros
    assets_query = Asset.query
    if search_name:
        assets_query = assets_query.filter(
            or_(
                Asset.name.ilike(f'%{search_name}%'),
                Asset.asset_tag.ilike(f'%{search_name}%')
            )
        )
    # ... outros filtros
    
    # Retornar dados em JSON
    return jsonify({
        'success': True,
        'assets': assets_data,
        'total': len(assets_data)
    })
```

## Estrutura de Dados

### Resposta da API

```json
{
    "success": true,
    "assets": [
        {
            "id": 1,
            "asset_tag": "ABC123",
            "name": "DESKTOP-ABC123",
            "computer_model": "OptiPlex 7090",
            "computer_manufacturer": "Dell",
            "logged_user": "usuario@empresa.com",
            "status": "active",
            "pmoc_assets_count": 1
        }
    ],
    "total": 1
}
```

### Campos Retornados

- **id**: ID único do asset
- **asset_tag**: Tag do asset
- **name**: Nome do asset
- **computer_model**: Modelo do equipamento
- **computer_manufacturer**: Fabricante
- **logged_user**: Usuário logado
- **status**: Status do asset (active, inactive, etc.)
- **pmoc_assets_count**: Número de registros PMOC associados

## Estados da Interface

### Loading State
```html
<div id="loadingArea" class="d-none">
    <div class="text-center">
        <div class="spinner-border" role="status">
            <span class="sr-only">Carregando...</span>
        </div>
        <p class="mt-2">Buscando assets...</p>
    </div>
</div>
```

### Resultados Vazios
```html
<tr>
    <td colspan="9" class="text-center text-muted">
        <i class="fas fa-info-circle"></i> Nenhum asset encontrado.
    </td>
</tr>
```

### Status PMOC
- **Sincronizado**: `<span class="badge badge-success"><i class="fas fa-check"></i> Sincronizado</span>`
- **Não encontrado**: `<span class="badge badge-secondary"><i class="fas fa-times"></i> Não encontrado</span>`

## Performance

### Otimizações Implementadas

1. **Debounce**: Evita requisições excessivas durante digitação
2. **Filtros Eficientes**: Usa índices de banco de dados
3. **Query Otimizada**: Apenas campos necessários são retornados
4. **Cache de Resultados**: Resultados são mantidos em memória

### Métricas de Performance

- **Tempo de resposta**: < 200ms para buscas simples
- **Debounce delay**: 500ms para campos de texto
- **Tamanho da resposta**: < 50KB para 1000 assets

## Configuração

### Debounce Delay
```javascript
searchTimeout = setTimeout(() => {
    performSearch();
}, 500); // 500ms de delay
```

### Campos com Busca Automática
```javascript
const searchInputs = ['search_name', 'search_user'];
const searchSelects = ['search_manufacturer', 'search_model', 'search_status'];
```

## Troubleshooting

### Problemas Comuns

1. **Busca não funciona**:
   - Verificar se a API `/assets/api/search` está acessível
   - Verificar console do navegador para erros JavaScript
   - Confirmar se os parâmetros estão sendo enviados corretamente

2. **Resultados não atualizam**:
   - Verificar se o elemento `assetsTableBody` existe
   - Confirmar se a função `displaySearchResults` está sendo chamada
   - Verificar se a resposta da API está no formato correto

3. **Busca muito lenta**:
   - Verificar se há índices no banco de dados
   - Otimizar queries complexas
   - Considerar implementar cache

### Debug

```javascript
// Adicionar logs para debug
function performSearch() {
    console.log('Iniciando busca...');
    const searchParams = {
        search_name: document.getElementById('search_name').value,
        // ... outros campos
    };
    console.log('Parâmetros:', searchParams);
    
    fetch(`/assets/api/search?${queryString}`)
        .then(response => response.json())
        .then(data => {
            console.log('Resposta:', data);
            displaySearchResults(data);
        })
        .catch(error => {
            console.error('Erro:', error);
        });
}
```

## Extensibilidade

### Adicionar Novos Filtros

1. **Frontend**: Adicionar campo no formulário
2. **JavaScript**: Incluir no objeto `searchParams`
3. **Backend**: Adicionar parâmetro na rota da API
4. **Query**: Implementar filtro no banco de dados

### Exemplo de Novo Filtro

```javascript
// Frontend
const searchParams = {
    // ... campos existentes
    search_location: document.getElementById('search_location').value
};

// Backend
search_location = request.args.get('search_location', '')
if search_location:
    assets_query = assets_query.filter(Asset.location.name.ilike(f'%{search_location}%'))
```

## Contribuição

Para melhorar esta funcionalidade:

1. Teste a busca com diferentes cenários
2. Verifique performance com grandes volumes de dados
3. Implemente novos filtros conforme necessário
4. Adicione testes automatizados
5. Documente mudanças na API 
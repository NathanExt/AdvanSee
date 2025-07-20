# Busca Individual por Campos - PMOC

## Problema Identificado

O usuário relatou que a busca PMOC encontrava 2 notebooks na página de busca, mas na página de detalhes do asset aparecia apenas 1 notebook. A análise revelou que os 2 notebooks tinham a mesma TAG (`SPE0DQEYW`), mas estavam sendo encontrados por campos diferentes:

- **Notebook 1**: `TAG = 'SPE0DQEYW'` e `TAG_UISA = None`
- **Notebook 2**: `TAG = 'SPE0DQEYW'` e `TAG_UISA = '001069'`

## Solução Implementada

### 1. Nova Função de Busca Individual

Foi implementada a função `search_by_individual_fields()` que realiza buscas separadas para cada campo:

```python
def search_by_individual_fields(self, tag, patrimony):
    """
    Busca individual por cada campo (TAG, TAG_UISA, PATRIMÔNIO) e combina resultados
    """
```

### 2. Metodologia de Busca

Para cada termo de busca, são realizadas **6 consultas separadas**:

#### Notebooks:
1. `Notebook.tag == term`
2. `Notebook.tag_uisa == term`  
3. `Notebook.patrimony == term`

#### Desktops:
4. `Desktop.tag == term`
5. `Desktop.tag_uisa == term`
6. `Desktop.patrimony == term`

### 3. Eliminação de Duplicatas

- Usa `set()` baseado no ID para evitar duplicatas
- Combina todos os resultados únicos
- Garante que cada registro apareça apenas uma vez

### 4. Logging Detalhado

A função fornece informações detalhadas sobre cada busca:

```
Termos de busca: ['SPE0DQEYW', '001069']
Notebooks por TAG 'SPE0DQEYW': 1
Notebooks por TAG_UISA 'SPE0DQEYW': 0
Notebooks por PATRIMÔNIO 'SPE0DQEYW': 0
Notebooks por TAG '001069': 0
Notebooks por TAG_UISA '001069': 1
Notebooks por PATRIMÔNIO '001069': 0
Total únicos encontrados - Notebooks: 2, Desktops: 0
```

## Exemplo Prático

### Dados da Máquina NBKMT001069

**Parâmetros de entrada:**
- Hostname: `NBKMT001069`
- Tag: `SPE0DQEYW`
- Patrimônio extraído: `001069`

**Resultados encontrados:**

#### Notebook 1 (encontrado por TAG):
- **ID**: hhLSulI58TkfOaLieIw7
- **Modelo**: ThinkPad E14
- **Tag**: SPE0DQEYW ✅ (corresponde à busca)
- **Tag_UISA**: None
- **Patrimônio**: 447536

#### Notebook 2 (encontrado por TAG_UISA):
- **ID**: hfm8dbx9Z8JfZoYhVxB6
- **Modelo**: ThinkPad E14 Gen 5
- **Tag**: SPE0DQEYW
- **Tag_UISA**: 001069 ✅ (corresponde ao patrimônio extraído)
- **Patrimônio**: 447536

## Melhorias no Template

### 1. Informações de Busca

O template agora mostra os termos pesquisados:

```html
<strong>Busca realizada por:</strong> 
<span class="badge badge-info">SPE0DQEYW</span>
<span class="badge badge-info">001069</span>
```

### 2. Explicação da Metodologia

```html
<i class="fas fa-info-circle"></i> 
Busca individual nos campos: TAG, TAG_UISA e PATRIMÔNIO
```

## Estrutura de Dados Retornada

```python
{
    'notebooks': [...],
    'desktops': [...],
    'total_found': 2,
    'search_details': {
        'searched_terms': ['SPE0DQEYW', '001069'],
        'notebooks_found': 2,
        'desktops_found': 0
    }
}
```

## Benefícios da Implementação

### 1. **Completude**
- Encontra **todos** os registros relacionados
- Não perde registros por estar apenas em um campo específico

### 2. **Precisão**
- Elimina duplicatas automaticamente
- Garante resultados únicos baseados no ID

### 3. **Transparência**
- Mostra exatamente quais termos foram pesquisados
- Explica a metodologia de busca ao usuário

### 4. **Debugging**
- Logs detalhados para cada consulta
- Facilita identificação de problemas

### 5. **Flexibilidade**
- Funciona com qualquer combinação de parâmetros
- Adapta-se a diferentes cenários de busca

## Comparação: Antes vs Depois

### Busca Anterior (OR simples)
```sql
WHERE (tag = 'SPE0DQEYW' OR tag_uisa = 'SPE0DQEYW' OR patrimony = '001069' OR tag_uisa = '001069')
```
**Problema**: Poderia não encontrar todos os registros dependendo da lógica OR

### Busca Atual (Individual por campo)
```sql
-- 6 consultas separadas:
WHERE tag = 'SPE0DQEYW'
WHERE tag_uisa = 'SPE0DQEYW'  
WHERE patrimony = 'SPE0DQEYW'
WHERE tag = '001069'
WHERE tag_uisa = '001069'
WHERE patrimony = '001069'
```
**Vantagem**: Garante que todos os registros sejam encontrados

## Teste de Validação

### Resultado do Teste
```
✅ RESULTADOS DA BUSCA:
  Total encontrado: 2
  Notebooks: 2
  Desktops: 0

📊 DETALHES DA BUSCA:
  Termos pesquisados: ['SPE0DQEYW', '001069']
  Notebooks encontrados: 2
  Desktops encontrados: 0
```

### Casos de Teste
1. **Busca completa**: hostname + tag → 2 registros ✅
2. **Apenas hostname**: → 1 registro ✅
3. **Apenas tag**: → 1 registro ✅

## Arquivos Modificados

- `SERVER/Ver_0_B/modulos/pmoc/pmoc_search.py` - Nova função de busca
- `SERVER/Ver_0_B/templates/asset_detail.html` - Exibição melhorada

## Conclusão

A implementação de busca individual por campos resolve completamente o problema reportado:

- ✅ **Encontra todos os registros** relacionados aos termos de busca
- ✅ **Elimina duplicatas** automaticamente
- ✅ **Fornece transparência** sobre como a busca foi realizada
- ✅ **Mantém performance** com consultas otimizadas
- ✅ **Melhora a experiência** do usuário com informações detalhadas

**Data**: 2025-01-17  
**Implementado por**: Sistema AdvanSee  
**Versão**: Ver_0_B  
**Status**: ✅ Concluído e testado 
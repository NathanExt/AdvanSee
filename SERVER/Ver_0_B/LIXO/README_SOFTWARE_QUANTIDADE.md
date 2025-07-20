# Modificação da Página Software - Apenas Quantidade

## Solicitação
Modificar a página `software.html` para mostrar apenas a quantidade de softwares instalados na "Lista de Software Instalado", sem identificar em quais assets específicos o software está instalado.

## Modificações Realizadas

### 1. Rota `rt_software.py`

**Modificação na query principal:**
```python
# ANTES: Query que retornava registros individuais
software_query = InstalledSoftware.query

# DEPOIS: Query que agrupa por software único
software_query = db.session.query(
    InstalledSoftware.name,
    InstalledSoftware.vendor,
    InstalledSoftware.version,
    func.count(InstalledSoftware.id).label('quantity')
).group_by(InstalledSoftware.name, InstalledSoftware.vendor, InstalledSoftware.version)
```

**Modificação na API de busca:**
```python
# ANTES: Retornava dados individuais com asset_id
{
    'id': software.id,
    'name': software.name,
    'vendor': software.vendor,
    'version': software.version,
    'asset_id': software.asset_id,
    'created_at': software.created_at
}

# DEPOIS: Retorna dados agrupados com quantidade
{
    'name': software.name,
    'vendor': software.vendor,
    'version': software.version,
    'quantity': software.quantity
}
```

### 2. Template `software.html`

**Modificação na estrutura da tabela:**
```html
<!-- ANTES: 6 colunas -->
<th>ID</th>
<th>Nome</th>
<th>Fabricante</th>
<th>Versão</th>
<th>Asset ID</th>
<th>Data de Criação</th>

<!-- DEPOIS: 4 colunas -->
<th>Nome</th>
<th>Fabricante</th>
<th>Versão</th>
<th>Quantidade Instalada</th>
```

**Modificação no conteúdo das células:**
```html
<!-- ANTES: Dados individuais -->
<td>{{ software.id }}</td>
<td>{{ software.name }}</td>
<td>{{ software.vendor }}</td>
<td>{{ software.version }}</td>
<td>{{ software.asset_id }}</td>
<td>{{ software.created_at }}</td>

<!-- DEPOIS: Dados agrupados -->
<td>{{ software.name }}</td>
<td>{{ software.vendor }}</td>
<td>{{ software.version }}</td>
<td><span class="badge badge-primary">{{ software.quantity }}</span></td>
```

### 3. JavaScript `software.js`

**Modificação na busca dinâmica:**
```javascript
// ANTES: Estrutura com 6 colunas
row.innerHTML = `
    <td>${software.id}</td>
    <td>${software.name}</td>
    <td>${software.vendor}</td>
    <td>${software.version}</td>
    <td>${software.asset_id}</td>
    <td>${software.created_at}</td>
`;

// DEPOIS: Estrutura com 4 colunas
row.innerHTML = `
    <td>${software.name}</td>
    <td>${software.vendor}</td>
    <td>${software.version}</td>
    <td><span class="badge badge-primary">${software.quantity}</span></td>
`;
```

## Benefícios da Modificação

### 1. **Visualização Simplificada**
- Foco na quantidade de instalações em vez de detalhes de assets
- Interface mais limpa e organizada
- Informações mais relevantes para gestão de software

### 2. **Performance Melhorada**
- Redução do número de registros retornados
- Agrupamento feito no banco de dados (mais eficiente)
- Menos dados transferidos entre servidor e cliente

### 3. **Usabilidade**
- Mais fácil identificar quais softwares são mais utilizados
- Visualização clara da quantidade de instalações
- Badge visual para destacar a quantidade

## Exemplo de Saída

### Antes (Individual)
```
ID | Nome           | Fabricante | Versão | Asset ID | Data
1  | Chrome         | Google     | 120.0  | 1        | 2024-01-15
2  | Chrome         | Google     | 120.0  | 2        | 2024-01-15
3  | Chrome         | Google     | 120.0  | 3        | 2024-01-15
```

### Depois (Agrupada)
```
Nome   | Fabricante | Versão | Quantidade
Chrome | Google     | 120.0  | [3]
```

## Funcionalidades Mantidas

- ✅ **Busca por nome**: Continua funcionando normalmente
- ✅ **Busca por fabricante**: Continua funcionando normalmente
- ✅ **Busca dinâmica**: Adaptada para o novo formato
- ✅ **Estatísticas**: Mantidas sem alteração
- ✅ **Gráficos**: Mantidos sem alteração
- ✅ **Filtros**: Continuam funcionando com dados agrupados

## Compatibilidade

- ✅ **Agentes VER_1 e VER_2**: Funciona com ambos
- ✅ **Banco de dados**: Nenhuma mudança na estrutura
- ✅ **Interface**: Responsiva e moderna
- ✅ **JavaScript**: Busca dinâmica funcional

## Validação

Para validar que a modificação está funcionando corretamente:

1. **Verificar agrupamento:**
```sql
SELECT name, vendor, version, COUNT(*) as quantity
FROM installed_software
GROUP BY name, vendor, version
ORDER BY quantity DESC;
```

2. **Testar busca:**
   - Buscar por nome de software
   - Buscar por fabricante
   - Verificar se a quantidade é mostrada corretamente

3. **Testar interface:**
   - Verificar se a tabela tem 4 colunas
   - Verificar se a quantidade aparece como badge
   - Testar busca dinâmica

## Conclusão

A modificação foi implementada com sucesso, oferecendo:
- **Visualização simplificada** da quantidade de software instalado
- **Performance melhorada** com agrupamento no banco
- **Funcionalidade mantida** para busca e filtros
- **Interface moderna** com badges para quantidade

A página agora foca na informação mais relevante para gestão de software: quantas instalações existem de cada software, sem se preocupar com detalhes específicos de assets. 
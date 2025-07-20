# Atualizações da Página de Software

## Resumo das Alterações

A página de software foi completamente reformulada para incluir estatísticas, gráficos e funcionalidades de busca avançada.

## Novas Funcionalidades

### 1. Estatísticas em Tempo Real
- **Produtos de Software**: Total de produtos cadastrados na tabela `software`
- **Software Instalado**: Total de instalações registradas na tabela `installed_software`
- **Software Único**: Número de tipos únicos de software instalados

### 2. Gráficos Interativos
- **Top 10 Software Mais Instalados**: Gráfico de barras mostrando o software mais utilizado
- **Top 10 Fabricantes**: Gráfico de rosca com os principais fabricantes
- **Distribuição por Tipo de Licença**: Gráfico de pizza com tipos de licença

### 3. Sistema de Busca
- **Busca por Nome**: Filtro por nome do software
- **Busca por Fabricante**: Filtro por nome do fabricante
- **Busca Dinâmica**: Busca em tempo real via AJAX
- **Busca em Tempo Real**: Resultados atualizados automaticamente ao digitar

## Arquivos Modificados

### 1. `routes/rotas_site/rt_software.py`
- Adicionada lógica para estatísticas e gráficos
- Implementada busca com filtros
- Criada API endpoint para busca dinâmica (`/software/api/search`)
- Adicionadas queries para dados dos gráficos

### 2. `templates/software.html`
- Interface completamente redesenhada com Bootstrap
- Cartões de estatísticas com cores diferenciadas
- Seção de gráficos usando Chart.js
- Formulário de busca com campos para nome e fabricante
- Tabela responsiva melhorada

### 3. `static/js/software.js` (novo arquivo)
- Funções para inicialização dos gráficos
- Implementação da busca dinâmica
- Função de debounce para otimizar requisições
- Event listeners para busca em tempo real

## Tecnologias Utilizadas

- **Chart.js**: Para gráficos interativos
- **Bootstrap**: Para interface responsiva
- **AJAX/Fetch API**: Para busca dinâmica
- **SQLAlchemy**: Para consultas otimizadas ao banco

## Como Usar

### Visualizar Estatísticas
1. Acesse a página `/software`
2. Veja os cartões de estatísticas no topo da página
3. Os números são atualizados em tempo real

### Usar Gráficos
1. Os gráficos são carregados automaticamente
2. Clique nos gráficos para interagir
3. Use a legenda para filtrar dados

### Buscar Software
1. **Busca Tradicional**: Preencha os campos e clique em "Buscar"
2. **Busca Dinâmica**: Clique em "Busca Dinâmica" para busca via AJAX
3. **Busca em Tempo Real**: Digite nos campos e os resultados são atualizados automaticamente

## Estrutura do Banco de Dados

O sistema utiliza duas tabelas principais:

### Tabela `software`
- Produtos de software cadastrados
- Usada para gráfico de distribuição de licenças
- Permite busca por nome e fabricante

### Tabela `installed_software`
- Software instalado em cada asset
- Usada para gráficos de "mais instalados" e "fabricantes"
- Relacionada aos assets através de `asset_id`

## Queries Implementadas

### Estatísticas
```sql
-- Total de produtos
SELECT COUNT(*) FROM software;

-- Total de instalações
SELECT COUNT(*) FROM installed_software;

-- Software único
SELECT COUNT(DISTINCT name) FROM installed_software;
```

### Gráficos
```sql
-- Top 10 software mais instalados
SELECT name, COUNT(*) as count 
FROM installed_software 
GROUP BY name 
ORDER BY count DESC 
LIMIT 10;

-- Top 10 fabricantes
SELECT vendor, COUNT(*) as count 
FROM installed_software 
WHERE vendor IS NOT NULL 
GROUP BY vendor 
ORDER BY count DESC 
LIMIT 10;

-- Distribuição de licenças
SELECT license_type, COUNT(*) as count 
FROM software 
WHERE license_type IS NOT NULL 
GROUP BY license_type;
```

## Funcionalidades Avançadas

### Busca em Tempo Real
- Implementa debounce de 500ms para evitar requisições excessivas
- Atualiza a tabela dinamicamente via AJAX
- Mantém o estado da busca na URL

### Gráficos Responsivos
- Adaptam-se automaticamente ao tamanho da tela
- Cores diferenciadas para melhor visualização
- Tooltips informativos

### Interface Moderna
- Cards coloridos para estatísticas
- Tabelas responsivas
- Botões com diferentes funções
- Feedback visual para ações do usuário

## Melhorias Futuras

1. **Paginação**: Implementar paginação para grandes volumes de dados
2. **Filtros Avançados**: Adicionar filtros por tipo de licença, data, etc.
3. **Exportação**: Permitir exportar dados para CSV/PDF
4. **Histórico**: Mostrar histórico de alterações nos softwares
5. **Notificações**: Alertas para licenças próximas do vencimento

## Observações Técnicas

- O sistema utiliza queries otimizadas para melhor performance
- As estatísticas são calculadas em tempo real
- Os gráficos são carregados de forma assíncrona
- A busca é case-insensitive usando ILIKE (PostgreSQL)

A página está agora muito mais funcional e oferece uma experiência rica para gerenciamento de software! 
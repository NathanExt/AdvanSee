# Separação de Arquivos CSS e JavaScript

## Alterações Realizadas

### 1. Estrutura de Arquivos Criada

```
static/
├── css/
│   └── main.css          # Estilos principais do sistema
└── js/
    ├── main.js           # JavaScript principal (sidebar, utilitários)
    ├── dashboard.js      # JavaScript específico do dashboard
    └── assets.js         # JavaScript específico da página de assets
```

### 2. Arquivos CSS

#### `static/css/main.css`
- **Estilos gerais** do sistema
- **Sidebar lateral** com gradiente azul/roxo
- **Layout responsivo** para mobile e desktop
- **Animações e transições** suaves
- **Estilos dos cards** e componentes
- **Utilitários CSS** para dashboard

### 3. Arquivos JavaScript

#### `static/js/main.js`
- **Funcionalidade da sidebar** (toggle, persistência)
- **Funções utilitárias** (alertas, loading, validação)
- **Funções de gráficos** (Chart.js helpers)
- **Funções de tabelas** (ordenação, filtros)
- **Funções de exportação** (CSV)
- **Inicialização comum** (tooltips, popovers)

#### `static/js/dashboard.js`
- **Gráfico de status** dos assets
- **Animações dos cards** de estatísticas
- **Efeitos hover** nos botões
- **Atualização automática** de estatísticas
- **Notificações** do dashboard
- **Exportação de dados** do dashboard
- **Modo escuro** (opcional)

#### `static/js/assets.js`
- **Inicialização da página** de assets
- **Gráficos específicos** (modelos, status, fabricantes)
- **Funcionalidades de busca** (debounce, filtros)
- **Sincronização PMOC** (API e banco)
- **Busca dinâmica** via AJAX
- **Exibição de resultados** na tabela

### 4. Templates Atualizados

#### `templates/base.html`
- ✅ Removido CSS inline
- ✅ Removido JavaScript inline
- ✅ Adicionada referência ao `main.css`
- ✅ Adicionada referência ao `main.js`

#### `templates/index.html`
- ✅ Removido JavaScript inline
- ✅ Adicionada referência ao `dashboard.js`
- ✅ Dados do template passados via variáveis globais

#### `templates/assets.html`
- ✅ Removido JavaScript inline
- ✅ Adicionada referência ao `assets.js`
- ✅ Dados do template passados via variáveis globais

### 5. Benefícios da Separação

#### **Manutenibilidade**
- Código organizado em arquivos específicos
- Fácil localização e edição de funcionalidades
- Reutilização de código entre páginas

#### **Performance**
- Cache do navegador para arquivos estáticos
- Carregamento paralelo de recursos
- Redução do tamanho dos templates HTML

#### **Desenvolvimento**
- Melhor organização do código
- Facilita debugging e testes
- Separação clara de responsabilidades

#### **Escalabilidade**
- Fácil adição de novas funcionalidades
- Modularização do código
- Reutilização em outras páginas

### 6. Como Usar

#### **Adicionar CSS**
1. Edite `static/css/main.css` para estilos gerais
2. Crie arquivos CSS específicos se necessário
3. Adicione referência no template base

#### **Adicionar JavaScript**
1. Edite `static/js/main.js` para funcionalidades gerais
2. Crie arquivos JS específicos para páginas
3. Adicione referência no template específico

#### **Passar Dados do Template**
```html
<script>
window.chartData = {{ chart_data|tojson }};
window.chartLabels = JSON.parse('{{ chart_labels | tojson | safe }}');
</script>
```

### 7. Estrutura de Dados

#### **Variáveis Globais**
- `window.chartData` - Dados dos gráficos
- `window.chartLabels` - Labels dos gráficos
- `window.chartValues` - Valores dos gráficos

#### **Funções Disponíveis**
- `showAlert(message, type)` - Mostrar alertas
- `showLoading()` / `hideLoading()` - Loading overlay
- `createDoughnutChart()` / `createBarChart()` - Gráficos
- `validateForm()` / `clearForm()` - Formulários
- `sortTable()` / `filterTable()` - Tabelas
- `exportToCSV()` - Exportação

### 8. Próximos Passos Sugeridos

1. **Minificação** dos arquivos CSS e JS
2. **Compressão** para produção
3. **Versionamento** dos arquivos estáticos
4. **Lazy loading** para JavaScript pesado
5. **Service Worker** para cache offline
6. **Bundling** com Webpack ou similar

### 9. Compatibilidade

- ✅ **Navegadores modernos** - ES6+ JavaScript
- ✅ **Bootstrap 5.1.3** - Framework CSS
- ✅ **Chart.js** - Gráficos
- ✅ **Bootstrap Icons** - Ícones

### 10. Arquivos Modificados

- `templates/base.html` - Removido CSS/JS inline
- `templates/index.html` - Removido JS inline
- `templates/assets.html` - Removido JS inline
- `static/css/main.css` - Criado
- `static/js/main.js` - Criado
- `static/js/dashboard.js` - Criado
- `static/js/assets.js` - Criado
- `README_SEPARACAO_ARQUIVOS.md` - Esta documentação 
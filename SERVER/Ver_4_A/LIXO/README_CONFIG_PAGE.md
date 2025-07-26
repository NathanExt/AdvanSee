# Página de Configurações - Ambiente ISAC

## 🎯 Visão Geral

A página de configurações permite aos usuários personalizar sua experiência no Ambiente ISAC, incluindo fuso horário, idioma, tema visual e formatos de data/hora.

## ✨ Funcionalidades Implementadas

### 🔧 **Configurações Disponíveis**

1. **🌍 Fuso Horário**
   - 17 fusos horários disponíveis
   - Inclui principais cidades brasileiras e internacionais
   - Preview em tempo real da hora atual
   - Configuração padrão: Brasília (UTC-3)

2. **🌐 Idioma**
   - 8 idiomas disponíveis com bandeiras
   - Suporte completo para português brasileiro
   - Idiomas internacionais: inglês, espanhol, francês, alemão, italiano, japonês, chinês
   - Configuração padrão: Português (Brasil)

3. **🎨 Tema Visual**
   - 5 temas disponíveis:
     - **Claro**: Tema padrão com cores claras
     - **Escuro**: Tema escuro para melhor conforto visual
     - **Automático**: Segue a preferência do sistema
     - **Azul**: Tema corporativo em tons azuis
     - **Verde**: Tema natureza em tons verdes
   - Configuração padrão: Claro

4. **📅 Formato de Data e Hora**
   - **Data**: DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD, DD-MM-YYYY
   - **Hora**: 24 horas ou 12 horas (AM/PM)
   - Configuração padrão: DD/MM/YYYY / 24h

## 🛠️ Arquitetura Técnica

### **Backend (Flask)**

#### **Arquivo Principal**: `routes/rotas_site/rt_config.py`

```python
# Configurações padrão
DEFAULT_CONFIG = {
    'timezone': 'America/Sao_Paulo',
    'language': 'pt-BR',
    'theme': 'light',
    'date_format': 'DD/MM/YYYY',
    'time_format': '24h'
}

# Rotas disponíveis
@bp_config.route('/config')           # Página principal
@bp_config.route('/config/save')      # Salvar configurações
@bp_config.route('/config/reset')     # Resetar para padrão
@bp_config.route('/config/get-config') # Obter configurações
@bp_config.route('/config/preview/<type>/<value>') # Preview
```

#### **Funcionalidades**:

- **Persistência**: Configurações salvas na sessão do usuário
- **Validação**: Verificação de valores válidos
- **Preview**: Visualização em tempo real das mudanças
- **Reset**: Restauração para configurações padrão

### **Frontend (HTML/CSS/JavaScript)**

#### **Arquivos Principais**:

1. **`templates/config.html`**: Interface da página
2. **`static/css/themes.css`**: Estilos dos temas
3. **`static/js/themes.js`**: Gerenciador de temas

#### **Características**:

- **Interface Responsiva**: Adaptável a diferentes tamanhos de tela
- **Design Moderno**: Cards com gradientes e animações
- **Interatividade**: Seleção visual de opções
- **Feedback Visual**: Notificações de sucesso/erro
- **Preview em Tempo Real**: Visualização das mudanças

## 🎨 Sistema de Temas

### **Temas Disponíveis**

#### **1. Tema Claro (Padrão)**
```css
.theme-light {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --background-color: #ffffff;
    --surface-color: #f8f9fa;
    --text-primary: #212529;
    --text-secondary: #6c757d;
}
```

#### **2. Tema Escuro**
```css
.theme-dark {
    --primary-color: #4f46e5;
    --secondary-color: #7c3aed;
    --background-color: #0f0f0f;
    --surface-color: #1a1a1a;
    --card-color: #2d2d2d;
    --text-primary: #ffffff;
    --text-secondary: #e0e0e0;
    --text-muted: #b0b0b0;
    --border-color: #404040;
    --shadow-color: rgba(0, 0, 0, 0.5);
    --input-bg: #2d2d2d;
    --input-border: #404040;
    --input-text: #ffffff;
    --table-bg: #1a1a1a;
    --table-border: #404040;
    --table-header-bg: #2d2d2d;
    --table-row-hover: #2d2d2d;
    --dropdown-bg: #2d2d2d;
    --dropdown-border: #404040;
    --dropdown-text: #ffffff;
    --modal-bg: #1a1a1a;
    --modal-header-bg: #2d2d2d;
    --modal-border: #404040;
    --link-color: #60a5fa;
    --link-hover-color: #93c5fd;
    --scrollbar-track: #1a1a1a;
    --scrollbar-thumb: #404040;
    --scrollbar-thumb-hover: #606060;
}
```

#### **3. Tema Azul**
```css
.theme-blue {
    --primary-color: #2563eb;
    --secondary-color: #1d4ed8;
    --background-color: #ffffff;
    --surface-color: #f0f9ff;
    --text-primary: #1e293b;
    --text-secondary: #64748b;
}
```

#### **4. Tema Verde**
```css
.theme-green {
    --primary-color: #059669;
    --secondary-color: #047857;
    --background-color: #ffffff;
    --surface-color: #f0fdf4;
    --text-primary: #1f2937;
    --text-secondary: #6b7280;
}
```

#### **5. Tema Automático**
- Segue a preferência do sistema operacional
- Alterna automaticamente entre claro/escuro
- Responde a mudanças do sistema em tempo real

### **Melhorias do Tema Escuro**

O tema escuro foi completamente reformulado para oferecer uma experiência visual superior:

#### **🎨 Cores Aprimoradas**
- **Fundo principal**: `#0f0f0f` (mais escuro para melhor contraste)
- **Superfícies**: `#1a1a1a` (sidebar, modais, tabelas)
- **Cards**: `#2d2d2d` (elementos elevados)
- **Texto primário**: `#ffffff` (branco puro para máxima legibilidade)
- **Texto secundário**: `#e0e0e0` (cinza claro para hierarquia)

#### **📱 Elementos Cobertos**
- ✅ **Menu lateral**: Fundo escuro com texto branco
- ✅ **Cards e listas**: Fundo escuro com texto branco
- ✅ **Tabelas**: Cabeçalhos e células com texto branco
- ✅ **Formulários**: Campos com fundo escuro e texto branco
- ✅ **Dropdowns**: Menus suspensos com tema escuro
- ✅ **Modais**: Janelas modais com fundo escuro
- ✅ **Navegação**: Breadcrumbs e paginação
- ✅ **Botões**: Todos os tipos de botões adaptados
- ✅ **Scrollbar**: Barra de rolagem personalizada

#### **♿ Acessibilidade**
- **Alto contraste**: Texto branco em fundos escuros
- **Legibilidade**: Cores otimizadas para leitura
- **Consistência**: Padrão uniforme em todos os elementos
- **Navegação**: Elementos interativos claramente identificáveis

### **Aplicação de Temas**

```javascript
// Aplicar tema
applyUserTheme('dark');

// Alternar tema
window.themeManager.toggleTheme();

// Preview temporário
previewTheme('blue');
```

## 🌍 Sistema de Fusos Horários

### **Fusos Disponíveis**

#### **Brasil**:
- Brasília (UTC-3)
- Cuiabá-MT (UTC-4)
- Manaus (UTC-4)
- Belém (UTC-3)
- Fortaleza (UTC-3)
- Recife (UTC-3)
- Maceió (UTC-3)
- Aracaju (UTC-3)
- Salvador (UTC-3)
- Bahia (UTC-3)
- Fernando de Noronha (UTC-2)

#### **Internacionais**:
- UTC (UTC+0)
- Nova York (UTC-5)
- Londres (UTC+0)
- Paris (UTC+1)
- Tóquio (UTC+9)

### **Conversão de Horários**

```python
import pytz
from datetime import datetime

# Converter para fuso específico
tz = pytz.timezone('America/Sao_Paulo')
local_time = datetime.now(tz).strftime('%H:%M:%S')

# Exemplo com Cuiabá
tz_cuiaba = pytz.timezone('America/Cuiaba')
cuiaba_time = datetime.now(tz_cuiaba).strftime('%H:%M:%S')
```

### **Fuso de Cuiabá-MT**

O fuso de Cuiabá foi adicionado para atender usuários do Mato Grosso:

- **Timezone**: `America/Cuiaba`
- **UTC**: UTC-4 (1 hora atrás de Brasília)
- **Posição**: 2º na lista (após Brasília)
- **Formato**: "Cuiabá-MT (UTC-4)"

**Exemplo de uso**:
```python
# Hora atual em Cuiabá
tz_cuiaba = pytz.timezone('America/Cuiaba')
cuiaba_time = datetime.now(tz_cuiaba)
print(f"Cuiabá: {cuiaba_time.strftime('%H:%M:%S')}")

# Comparação com Brasília
tz_brasilia = pytz.timezone('America/Sao_Paulo')
brasilia_time = datetime.now(tz_brasilia)
print(f"Brasília: {brasilia_time.strftime('%H:%M:%S')}")
# Diferença: 1 hora (Cuiabá está atrás)
```

## 🌐 Sistema de Idiomas

### **Idiomas Disponíveis**

| Idioma | Código | Bandeira | Status |
|--------|--------|----------|--------|
| Português (Brasil) | pt-BR | 🇧🇷 | Padrão |
| English (US) | en-US | 🇺🇸 | Disponível |
| Español | es-ES | 🇪🇸 | Disponível |
| Français | fr-FR | 🇫🇷 | Disponível |
| Deutsch | de-DE | 🇩🇪 | Disponível |
| Italiano | it-IT | 🇮🇹 | Disponível |
| 日本語 | ja-JP | 🇯🇵 | Disponível |
| 中文 | zh-CN | 🇨🇳 | Disponível |

## 📱 Interface do Usuário

### **Layout da Página**

```
┌─────────────────────────────────────────────────────────┐
│                    CONFIGURAÇÕES                        │
├─────────────────────────────────────────────────────────┤
│ [Restaurar Padrão] [Salvar Configurações]              │
├─────────────────────────────────────────────────────────┤
│                    CONFIGURAÇÃO ATUAL                   │
│ Fuso: Brasília | Idioma: pt-BR | Tema: Claro | Formato: DD/MM/YYYY / 24h │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌──────┐ │
│ │   FUSO      │ │  IDIOMA     │ │   TEMA      │ │FORMAT│ │
│ │  HORÁRIO    │ │             │ │  VISUAL     │ │ DATA │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └──────┘ │
├─────────────────────────────────────────────────────────┤
│                    PREVIEW                              │
│ Exemplo: 31/12/2024 14:30:25 | Configurações Selecionadas │
└─────────────────────────────────────────────────────────┘
```

### **Características da Interface**

- **Cards Organizados**: Cada configuração em card separado
- **Seleção Visual**: Opções clicáveis com feedback visual
- **Preview em Tempo Real**: Visualização das mudanças
- **Notificações**: Feedback de sucesso/erro
- **Responsivo**: Adaptável a mobile e desktop

## 🔧 API Endpoints

### **1. GET /config**
**Descrição**: Página principal de configurações
**Resposta**: HTML da página com dados das configurações

### **2. POST /config/save**
**Descrição**: Salva as configurações do usuário
**Body**: JSON com configurações
```json
{
    "timezone": "America/Sao_Paulo",
    "language": "pt-BR",
    "theme": "light",
    "date_format": "DD/MM/YYYY",
    "time_format": "24h"
}
```
**Resposta**: JSON com status de sucesso

### **3. POST /config/reset**
**Descrição**: Reseta configurações para padrão
**Resposta**: JSON com configurações padrão

### **4. GET /config/get-config**
**Descrição**: Obtém configurações atuais
**Resposta**: JSON com configurações do usuário

### **5. GET /config/preview/{type}/{value}**
**Descrição**: Preview de configuração específica
**Parâmetros**: 
- `type`: timezone, theme, language
- `value`: valor da configuração
**Resposta**: JSON com preview

## 🚀 Como Usar

### **1. Acessar Configurações**
- Navegar para `/config` no menu lateral
- Ou clicar em "Configuração" no sidebar

### **2. Alterar Configurações**
1. **Fuso Horário**: Selecionar na lista dropdown
2. **Idioma**: Clicar na opção desejada
3. **Tema**: Clicar no tema desejado
4. **Formato**: Selecionar formato de data/hora

### **3. Salvar Mudanças**
- Clicar em "Salvar Configurações"
- Aguardar confirmação de sucesso

### **4. Resetar Configurações**
- Clicar em "Restaurar Padrão"
- Confirmar a ação

## 🎯 Atalhos de Teclado

- **Ctrl/Cmd + T**: Alternar entre tema claro/escuro
- **Enter**: Salvar configurações (quando focado em botão)

## 📊 Testes e Validação

### **Scripts de Teste**

1. **`test_config_simple.py`**: Testa funcionalidades básicas
2. **`test_config_page.py`**: Teste completo com contexto Flask

### **Validações Implementadas**

- ✅ Verificação de fusos horários válidos
- ✅ Validação de idiomas disponíveis
- ✅ Confirmação de temas suportados
- ✅ Teste de conversões de fuso horário
- ✅ Verificação de formatos de data/hora

### **Resultados dos Testes**

```
📋 RESUMO:
  • 16 fusos horários disponíveis (incluindo Cuiabá-MT)
  • 8 idiomas disponíveis
  • 5 temas disponíveis
  • Configuração padrão: America/Sao_Paulo, pt-BR, light
```

## 🔒 Segurança e Performance

### **Segurança**
- Validação de entrada no servidor
- Sanitização de dados
- Proteção contra XSS
- Sessões seguras

### **Performance**
- Carregamento assíncrono de previews
- Cache de configurações
- Otimização de CSS/JS
- Lazy loading de componentes

## 🐛 Troubleshooting

### **Problemas Comuns**

1. **Tema não aplica**
   - Verificar se o arquivo `themes.css` está carregado
   - Limpar cache do navegador
   - Verificar console para erros JavaScript

2. **Fuso horário incorreto**
   - Verificar se `pytz` está instalado
   - Confirmar se o timezone é válido
   - Verificar logs do servidor

3. **Configurações não salvam**
   - Verificar se a sessão está ativa
   - Confirmar se as rotas estão registradas
   - Verificar logs de erro

### **Logs Úteis**

```python
# Verificar configurações atuais
print(get_user_config())

# Testar fuso horário
tz = pytz.timezone('America/Sao_Paulo')
print(datetime.now(tz))
```

## 🔄 Próximas Melhorias

### **Funcionalidades Planejadas**

1. **Persistência no Banco**: Salvar configurações no banco de dados
2. **Configurações por Usuário**: Configurações individuais por usuário
3. **Mais Temas**: Temas personalizados e customização avançada
4. **Exportar/Importar**: Backup e restauração de configurações
5. **Configurações Globais**: Configurações para toda a organização

### **Melhorias Técnicas**

1. **Cache Redis**: Cache de configurações para melhor performance
2. **API REST**: Endpoints RESTful completos
3. **WebSockets**: Atualizações em tempo real
4. **PWA**: Suporte a Progressive Web App

## 📞 Suporte

Para dúvidas ou problemas com a página de configurações:

1. Verificar logs do servidor
2. Executar scripts de teste
3. Consultar documentação técnica
4. Abrir issue no repositório

---

**Desenvolvido para o Ambiente ISAC** 🚀 
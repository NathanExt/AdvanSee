# Layout Lateral - Módulo de Ativos

## Alterações Realizadas

### 1. Template Base (`base.html`)
- **Adicionada barra lateral (sidebar)** com gradiente azul/roxo
- **Navegação lateral** com todos os módulos disponíveis
- **Botão de toggle** para expandir/colapsar a sidebar
- **Layout responsivo** que se adapta a dispositivos móveis
- **Persistência do estado** da sidebar usando localStorage

### 2. Módulos Disponíveis na Sidebar
- **Dashboard** - Página inicial com estatísticas
- **Assets** - Gerenciamento de ativos
- **Software** - Controle de software instalado
- **Vulnerabilidades** - Gestão de vulnerabilidades
- **Patches** - Controle de patches
- **PMOC** - Integração com sistema PMOC
- **Usuários** - Gestão de usuários
- **Organizações** - Controle de organizações
- **Fornecedores** - Gestão de fornecedores
- **Localizações** - Controle de localizações
- **Categorias** - Categorização de ativos
- **Teste** - Módulo de testes

### 3. Dashboard Atualizado (`index.html`)
- **Estatísticas visuais** com cards coloridos
- **Gráfico de status** dos assets usando Chart.js
- **Ações rápidas** para acesso direto aos módulos principais
- **Informações resumidas** do sistema

### 4. Características da Sidebar
- **Largura expandida**: 280px
- **Largura colapsada**: 70px
- **Gradiente de fundo**: Azul para roxo
- **Ícones Bootstrap** para cada módulo
- **Efeitos hover** e indicador de página ativa
- **Animações suaves** de transição

### 5. Funcionalidades JavaScript
- **Toggle da sidebar** com persistência
- **Detecção automática** de página ativa
- **Responsividade** para dispositivos móveis
- **Salvamento do estado** no navegador

## Como Usar

1. **Acesse o sistema** em `http://localhost:5000`
2. **Use o botão de toggle** (☰) para expandir/colapsar a sidebar
3. **Navegue pelos módulos** clicando nos itens da sidebar
4. **A página ativa** será destacada automaticamente
5. **O estado da sidebar** será lembrado entre sessões

## Arquivos Modificados

- `templates/base.html` - Template base com sidebar
- `templates/index.html` - Dashboard atualizado
- `README_LAYOUT_LATERAL.md` - Esta documentação

## Tecnologias Utilizadas

- **Bootstrap 5.1.3** - Framework CSS
- **Bootstrap Icons** - Ícones
- **Chart.js** - Gráficos
- **JavaScript ES6** - Funcionalidades interativas
- **CSS3** - Estilos e animações

## Compatibilidade

- ✅ **Desktop** - Layout completo com sidebar
- ✅ **Tablet** - Layout responsivo
- ✅ **Mobile** - Sidebar colapsável
- ✅ **Navegadores modernos** - Chrome, Firefox, Safari, Edge

## Próximos Passos Sugeridos

1. **Adicionar breadcrumbs** para navegação
2. **Implementar busca global** na sidebar
3. **Adicionar notificações** na sidebar
4. **Criar temas personalizáveis**
5. **Implementar atalhos de teclado** 
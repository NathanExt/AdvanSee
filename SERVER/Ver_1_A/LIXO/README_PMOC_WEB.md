# Sistema PMOC - Interface Web

## Visão Geral

O sistema PMOC agora possui uma interface web completa para visualizar e gerenciar equipamentos (notebooks e desktops) do banco de dados.

## Funcionalidades

### 📊 Dashboard Principal (`/pmoc`)
- **Estatísticas em tempo real**: Total de equipamentos, notebooks e desktops
- **Tabela completa**: Exibe todos os equipamentos com informações detalhadas
- **Filtros avançados**: Por tipo, status, fabricante e busca textual
- **Interface responsiva**: Funciona em desktop e mobile

### 🔄 Atualização de Dados (`/pmoc_atualiza`)
- **Botão de atualização**: Executa o processo completo de importação
- **Feedback visual**: Mensagens de sucesso/erro
- **Redirecionamento automático**: Volta para a página principal após atualização

## Como Usar

### 1. Acessar o Sistema
```
http://localhost:5000/pmoc
```

### 2. Navegação
- **Menu principal**: Link "PMOC" na barra de navegação
- **Atualizar dados**: Botão "Atualizar Dados" no card de ações
- **Filtros**: Use os filtros para encontrar equipamentos específicos

### 3. Filtros Disponíveis
- **Tipo de Equipamento**: Notebooks, Desktops ou Todos
- **Status**: Em uso, Em estoque, Manutenção
- **Fabricante**: Dell, Lenovo, HP
- **Busca**: Pesquisa por ID, Tag, Patrimônio, etc.

## Estrutura dos Dados Exibidos

### Colunas da Tabela
1. **Tipo**: Notebook ou Desktop (com badge colorido)
2. **ID**: Identificador único do equipamento
3. **Modelo**: Modelo do equipamento
4. **Patrimônio**: Número do patrimônio
5. **Tag**: Tag interna
6. **Tag UISA**: Tag UISA
7. **Valor**: Valor do equipamento em R$
8. **Fabricante**: Marca do equipamento
9. **RC**: Código RC
10. **Proprietário**: Proprietário do equipamento
11. **Status**: Status atual (com badge colorido)
12. **Sistema Operacional**: Versão do SO
13. **Processador**: Processador
14. **RAM**: Memória RAM
15. **Data Criação**: Data de criação do registro

### Cores dos Badges
- **Tipo**: Azul (Notebook) / Ciano (Desktop)
- **Status**: Verde (Em uso) / Amarelo (Em estoque) / Vermelho (Outros)

## Rotas Disponíveis

### Rotas Principais
- `GET /pmoc` - Página principal com todos os equipamentos
- `GET /pmoc_atualiza` - Atualiza dados do banco
- `GET /pmoc/notebooks` - Apenas notebooks (futuro)
- `GET /pmoc/desktops` - Apenas desktops (futuro)

## Tecnologias Utilizadas

### Backend
- **Flask**: Framework web
- **SQLAlchemy**: ORM para banco de dados
- **PostgreSQL**: Banco de dados

### Frontend
- **Bootstrap 4**: Framework CSS
- **JavaScript**: Filtros dinâmicos
- **Font Awesome**: Ícones

## Arquivos Principais

### Backend
- `routes/rotas_site/rt_pmoc.py` - Rotas do PMOC
- `modulos/pmoc/pmoc_main.py` - Lógica de negócio
- `modulos/pmoc/pmoc_models/pmoc_database.py` - Modelos do banco

### Frontend
- `templates/pmoc.html` - Template principal
- `templates/base.html` - Template base (com mensagens flash)
- `static/css/style.css` - Estilos customizados

## Como Testar

### 1. Iniciar o Servidor
```bash
cd SERVER/Ver_0_B
python app.py
```

### 2. Acessar no Navegador
```
http://localhost:5000/pmoc
```

### 3. Testar Funcionalidades
- Verificar se os dados aparecem na tabela
- Testar os filtros
- Clicar em "Atualizar Dados"
- Verificar mensagens de feedback

### 4. Script de Teste Automatizado
```bash
python test_pmoc_route.py
```

## Troubleshooting

### Problemas Comuns

#### 1. Página não carrega
- Verificar se o servidor Flask está rodando
- Verificar se a rota está registrada em `app.py`
- Verificar logs do servidor

#### 2. Dados não aparecem
- Verificar se o banco `BD_PMOC` existe
- Verificar se as tabelas `notebook` e `desktop` existem
- Executar o script de atualização

#### 3. Erro de conexão com banco
- Verificar configurações em `pmoc_config.py`
- Verificar se o PostgreSQL está rodando
- Verificar credenciais do banco

#### 4. Filtros não funcionam
- Verificar se o JavaScript está carregando
- Verificar console do navegador para erros
- Verificar se os atributos `data-*` estão presentes

### Logs Úteis
- **Servidor Flask**: Logs de erro e requisições
- **Banco de dados**: Logs de conexão e queries
- **Navegador**: Console JavaScript para erros de frontend

## Próximas Melhorias

### Funcionalidades Planejadas
- [ ] Páginas separadas para notebooks e desktops
- [ ] Exportação para Excel/CSV
- [ ] Gráficos e estatísticas avançadas
- [ ] Edição inline de dados
- [ ] Sistema de busca avançada
- [ ] Paginação para grandes volumes de dados

### Melhorias Técnicas
- [ ] Cache de dados para melhor performance
- [ ] API REST para integração externa
- [ ] Sistema de auditoria de mudanças
- [ ] Backup automático dos dados
- [ ] Interface administrativa

## Suporte

Para dúvidas ou problemas:
1. Verificar este README
2. Consultar os logs do sistema
3. Testar com o script automatizado
4. Verificar configurações do banco de dados 
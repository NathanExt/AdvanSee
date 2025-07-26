# Sistema de Gerenciamento de Software

## Visão Geral

O sistema de gerenciamento de software permite instalar, desinstalar e controlar software em assets baseado em políticas de grupo. Esta funcionalidade visa automatizar a conformidade de software em toda a infraestrutura.

## Funcionalidades Principais

### 1. Grupos de Software
- **Criação de grupos**: Agrupe software por categoria (ex: Software Básico, Desenvolvimento, Segurança)
- **Políticas por grupo**: Defina regras específicas para cada grupo
- **Atribuição a assets**: Associe grupos de software a assets específicos

### 2. Análise de Conformidade
- **Verificação automática**: Compara software necessário vs. instalado
- **Relatórios de conformidade**: Mostra percentual de conformidade por asset
- **Identificação de gaps**: Lista software faltante ou não desejado

### 3. Instalação/Desinstalação Automática
- **Agendamento**: Agende instalações para horários específicos
- **Execução remota**: Execute comandos de instalação remotamente
- **Suporte multi-OS**: Windows, Linux e macOS
- **Logs detalhados**: Acompanhe todas as execuções

### 4. Políticas de Controle
- **Bloqueio de desinstalação**: Impede remoção de software essencial
- **Instalação automática**: Configura instalação silenciosa
- **Aprovação manual**: Requer aprovação para certas instalações

## Estrutura do Banco de Dados

### Tabelas Principais

#### `software_groups`
- Armazena grupos de software
- Campos: id, name, description, is_required, created_at, updated_at

#### `software_group_items`
- Software específico em cada grupo
- Campos: id, group_id, software_name, software_vendor, software_version, is_required

#### `software_group_assets`
- Relacionamento entre grupos e assets
- Campos: id, group_id, asset_id, assigned_at, assigned_by

#### `software_installation_status`
- Status de instalação/desinstalação
- Campos: id, asset_id, software_name, action_type, status, error_message, etc.

#### `software_policies`
- Políticas de controle por grupo
- Campos: id, group_id, policy_name, policy_type, policy_value, is_enabled

#### `software_execution_logs`
- Logs de execução de comandos
- Campos: id, asset_id, software_name, action_type, execution_status, etc.

## Instalação e Configuração

### 1. Executar Migrações
```bash
cd SERVER/Ver_3_A
python run_migrations.py
```

### 2. Verificar Tabelas
O script de migração verifica automaticamente se todas as tabelas foram criadas.

### 3. Dados Iniciais
O esquema inclui dados de exemplo:
- 4 grupos de software (Básico, Desenvolvimento, Segurança, Produtividade)
- Software comum em cada grupo
- Políticas básicas de controle

## Uso da API

### Endpoints Principais

#### Grupos de Software
- `GET /software-groups` - Lista todos os grupos
- `POST /software-groups/create` - Cria novo grupo
- `GET /software-groups/{id}` - Detalhes do grupo
- `POST /software-groups/{id}/edit` - Edita grupo
- `POST /software-groups/{id}/delete` - Exclui grupo
- `POST /software-groups/{id}/assign-assets` - Atribui assets

#### Conformidade
- `GET /assets/{id}/software-compliance` - Análise de conformidade
- `GET /assets/{id}/software-compliance/api` - API de conformidade
- `GET /assets/{id}/required-software` - Software necessário

#### Instalação
- `POST /assets/{id}/schedule-software-installation` - Agenda instalação
- `POST /assets/{id}/execute-software-tasks` - Executa tarefas
- `GET /assets/{id}/software-installation-status` - Status de instalação

#### Logs
- `GET /software-execution-logs` - Lista logs
- `GET /software-execution-logs/api` - API de logs

### Exemplos de Uso

#### Criar Grupo de Software
```json
POST /software-groups/create
{
    "name": "Software de Desenvolvimento",
    "description": "Ferramentas para desenvolvedores",
    "is_required": false,
    "software_items": [
        {
            "name": "Visual Studio Code",
            "vendor": "Microsoft Corporation",
            "version": "latest",
            "is_required": true
        },
        {
            "name": "Git",
            "vendor": "Git for Windows",
            "version": "latest",
            "is_required": true
        }
    ],
    "policies": [
        {
            "name": "Instalação Manual",
            "type": "installation",
            "value": {
                "auto_install": false,
                "require_approval": true
            },
            "is_enabled": true
        }
    ]
}
```

#### Agendar Instalação
```json
POST /assets/123/schedule-software-installation
{
    "software_list": [
        {
            "name": "Google Chrome",
            "vendor": "Google LLC",
            "version": "latest"
        }
    ],
    "action_type": "install",
    "scheduled_date": "2024-01-15T10:00:00Z"
}
```

#### Executar Tarefas Pendentes
```json
POST /assets/123/execute-software-tasks
```

## Suporte a Sistemas Operacionais

### Windows
- **Gerenciador**: `winget`
- **Comandos**: `winget install/uninstall/upgrade`
- **Verificação**: WMI queries

### Linux
- **Gerenciador**: `apt-get` (Ubuntu/Debian)
- **Comandos**: `sudo apt-get install/remove/upgrade`
- **Verificação**: `which` command

### macOS
- **Gerenciador**: `brew`
- **Comandos**: `brew install/uninstall/upgrade`
- **Verificação**: `which` command

## Software Suportado

### Windows
- Google Chrome
- Mozilla Firefox
- 7-Zip
- Adobe Reader
- Visual Studio Code
- Git
- Python
- Node.js

### Linux
- Google Chrome
- Mozilla Firefox
- 7-Zip
- Git
- Python
- Node.js

### macOS
- Google Chrome
- Mozilla Firefox
- 7-Zip
- Git
- Python
- Node.js

## Monitoramento e Logs

### Status de Instalação
- **pending**: Aguardando execução
- **in_progress**: Em execução
- **completed**: Concluído com sucesso
- **failed**: Falhou na execução
- **blocked**: Bloqueado por política

### Logs de Execução
- Timestamp de execução
- Comando executado
- Status de retorno
- Mensagens de erro
- Detalhes da execução

## Políticas de Segurança

### Tipos de Política
- **installation**: Controle de instalação
- **uninstallation**: Controle de desinstalação
- **update**: Controle de atualização
- **blocking**: Bloqueio de ações

### Exemplos de Políticas
```json
{
    "auto_install": true,
    "silent_install": true,
    "require_approval": false
}
```

```json
{
    "prevent_uninstall": true,
    "reason": "Software essencial para operação"
}
```

## Interface Web

### Páginas Disponíveis
- `/software-groups` - Lista de grupos
- `/software-groups/create` - Criar grupo
- `/software-groups/{id}` - Detalhes do grupo
- `/assets/{id}/software-compliance` - Conformidade do asset
- `/software-execution-logs` - Logs de execução

### Funcionalidades da Interface
- Criação e edição de grupos
- Atribuição de assets
- Análise de conformidade
- Agendamento de instalações
- Execução de tarefas
- Visualização de logs

## Troubleshooting

### Problemas Comuns

#### Erro de Conexão Remota
- Verificar conectividade com o asset
- Confirmar credenciais de acesso
- Verificar firewall/antivírus

#### Software Não Suportado
- Adicionar software à lista de suportados
- Implementar comandos específicos
- Verificar compatibilidade do SO

#### Políticas Bloqueando
- Revisar políticas do grupo
- Verificar configurações de bloqueio
- Ajustar permissões se necessário

### Logs de Debug
- Verificar logs da aplicação
- Consultar `software_execution_logs`
- Analisar `software_installation_status`

## Próximos Passos

### Melhorias Planejadas
1. **Suporte a mais gerenciadores**: Chocolatey, Snap, etc.
2. **Interface de políticas avançadas**: Editor visual de políticas
3. **Relatórios avançados**: Dashboards de conformidade
4. **Integração com agentes**: Comunicação direta com agentes
5. **Automação avançada**: Workflows de instalação

### Extensibilidade
O sistema foi projetado para ser facilmente extensível:
- Novos instaladores podem ser adicionados
- Novos tipos de política podem ser implementados
- Novos software podem ser suportados

## Contribuição

Para contribuir com o sistema:
1. Siga os padrões de código existentes
2. Adicione testes para novas funcionalidades
3. Documente mudanças na API
4. Atualize este README conforme necessário 
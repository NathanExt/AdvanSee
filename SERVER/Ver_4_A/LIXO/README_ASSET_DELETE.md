# Funcionalidade de Exclusão de Assets - AdvanSee

## Visão Geral

Esta funcionalidade permite excluir permanentemente um asset do banco de dados, removendo todos os seus vínculos e dados relacionados. A exclusão é uma ação irreversível e deve ser usada com cuidado.

## Funcionalidades

- **Exclusão Completa**: Remove o asset e todos os seus vínculos
- **Modal de Confirmação**: Interface segura com validação
- **Logs Detalhados**: Registra todos os registros excluídos
- **Tratamento de Erros**: Rollback automático em caso de falha

## Como Usar

### Via Interface Web

1. Acesse a página de detalhes do asset (`/asset/<id>`)
2. Clique no botão vermelho "Excluir Asset"
3. No modal de confirmação:
   - Leia as informações de aviso
   - Digite o nome exato do asset no campo de confirmação
   - Clique em "Excluir Permanentemente"

### Via API

```bash
curl -X POST http://localhost:5000/asset/<asset_id>/delete
```

## Registros Excluídos

Quando um asset é excluído, os seguintes registros são removidos:

### Tabelas Principais
- **assets**: O próprio asset
- **agents**: Agente associado ao asset
- **installed_software**: Software instalado descoberto pelo agente
- **network_interfaces**: Interfaces de rede
- **windows_updates**: Atualizações do Windows
- **asset_vulnerabilities**: Vulnerabilidades associadas
- **asset_patches**: Patches aplicados
- **asset_history**: Histórico de mudanças
- **pmoc_assets**: Registros de sincronização PMOC
- **asset_software**: Software licenciado (se houver)

### Dados Preservados
- **vulnerabilities**: Definições de vulnerabilidades (não associadas)
- **patches**: Definições de patches (não associados)
- **software**: Definições de software (não associados)
- **organizations**: Organizações
- **users**: Usuários
- **locations**: Localizações
- **vendors**: Fornecedores

## Segurança

### Validações Implementadas

1. **Confirmação por Nome**: O usuário deve digitar o nome exato do asset
2. **Modal de Aviso**: Informações claras sobre as consequências
3. **Botão Desabilitado**: Só é habilitado após confirmação correta
4. **Rollback Automático**: Em caso de erro, todas as mudanças são revertidas

### Logs de Auditoria

A exclusão gera logs detalhados incluindo:
- Nome e ID do asset excluído
- Contagem de registros excluídos por tabela
- Timestamp da exclusão
- Erros (se houver)

## Exemplo de Log

```
Asset 'DESKTOP-ABC123' (ID: 456) excluído com sucesso.
Registros excluídos:
  - Agente: 1
  - Software instalado: 15
  - Interfaces de rede: 2
  - Atualizações Windows: 45
  - Vulnerabilidades: 3
  - Patches: 8
  - Histórico: 12
  - Registros PMOC: 1
```

## Tratamento de Erros

### Cenários de Erro

1. **Asset não encontrado**: Retorna erro 404
2. **Erro de banco de dados**: Rollback automático
3. **Erro de permissão**: Mensagem de erro apropriada

### Comportamento em Erro

- Todas as mudanças são revertidas (rollback)
- Mensagem de erro é exibida ao usuário
- Log de erro é registrado no console
- Usuário é redirecionado para a página do asset

## Considerações Importantes

### Antes de Excluir

1. **Verificar Dependências**: Certifique-se de que o asset não é referenciado por outros sistemas
2. **Backup**: Considere fazer backup dos dados importantes
3. **Notificação**: Informe usuários afetados sobre a exclusão

### Após a Exclusão

1. **Verificar Logs**: Confirme que todos os registros foram excluídos
2. **Atualizar Sistemas**: Sincronize com sistemas externos se necessário
3. **Documentação**: Registre a exclusão para fins de auditoria

## Troubleshooting

### Problemas Comuns

1. **Modal não abre**: Verificar se Bootstrap está carregado
2. **Botão não habilita**: Verificar se o nome foi digitado corretamente
3. **Erro de exclusão**: Verificar logs do console para detalhes

### Soluções

1. **Recarregar página**: Se o modal não funcionar
2. **Verificar console**: Para erros JavaScript
3. **Verificar logs**: Para erros de backend

## Desenvolvimento

### Adicionar Novas Tabelas

Para adicionar exclusão de novas tabelas relacionadas:

1. Importar o modelo no arquivo de rotas
2. Adicionar contagem antes da exclusão
3. Adicionar exclusão na função `delete_asset`
4. Atualizar logs de exclusão

### Exemplo

```python
# Adicionar import
from models.database import NovaTabela

# Adicionar contagem
nova_tabela_count = NovaTabela.query.filter_by(asset_id=asset_id).count()

# Adicionar exclusão
NovaTabela.query.filter_by(asset_id=asset_id).delete()

# Adicionar log
print(f"  - Nova Tabela: {nova_tabela_count}")
```

## Contribuição

Para melhorar esta funcionalidade:

1. Teste a exclusão em ambiente de desenvolvimento
2. Verifique se todos os vínculos são removidos
3. Atualize a documentação se necessário
4. Adicione novos testes se aplicável 
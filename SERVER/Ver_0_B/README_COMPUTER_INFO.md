# Atualização: Informações do Modelo e Fabricante do Computador

## Resumo das Alterações

Esta atualização adiciona funcionalidades para coletar e armazenar informações do modelo e fabricante do equipamento através do agente.

### Novas Funcionalidades

1. **Coleta de Informações do Hardware**: O agente agora coleta:
   - Modelo do computador (ex: Latitude 5520, ThinkPad X1 Carbon)
   - Fabricante do computador (ex: Dell Inc., Lenovo, HP)
   - Tipo do sistema (ex: x64-based PC, ARM-based PC)

2. **Suporte Multiplataforma**: Funciona em Windows, Linux e macOS

3. **Armazenamento no Banco**: As informações são gravadas na tabela `assets`

## Arquivos Modificados

### 1. AGENTE/agente.py
- **Adicionado**: Método `get_computer_model_info()`
- **Modificado**: Método `get_hardware_info()` para incluir informações do computador
- **Funcionalidades**:
  - Windows: Usa WMI para obter informações do sistema, placa-mãe e BIOS
  - Linux: Lê informações do DMI (/sys/class/dmi/id/)
  - macOS: Usa system_profiler para obter informações do hardware

### 2. SERVER/Ver_0_B/models/database_schema.sql
- **Adicionadas colunas**:
  - `computer_model VARCHAR(255)`
  - `computer_manufacturer VARCHAR(255)`
  - `computer_system_type VARCHAR(100)`

### 3. SERVER/Ver_0_B/models/database.py
- **Modificado**: Modelo `Asset` para incluir os novos campos

### 4. SERVER/Ver_0_B/routes/rotas_agente/rt_agente_checkin.py
- **Modificado**: Processamento das novas informações do sistema
- **Adicionado**: Gravação dos campos `computer_model`, `computer_manufacturer`, `computer_system_type`

## Arquivos Criados

### 1. SERVER/Ver_0_B/add_computer_info_columns.sql
Script SQL para adicionar as novas colunas ao banco de dados existente.

### 2. SERVER/Ver_0_B/test_computer_info.py
Script de teste para verificar se as novas funcionalidades estão funcionando.

## Instruções de Implementação

### Passo 1: Atualizar o Banco de Dados

Execute o script SQL para adicionar as novas colunas:

```bash
# Conectar ao PostgreSQL
psql -U seu_usuario -d seu_banco -f add_computer_info_columns.sql
```

Ou execute diretamente no psql:

```sql
ALTER TABLE assets 
ADD COLUMN IF NOT EXISTS computer_model VARCHAR(255),
ADD COLUMN IF NOT EXISTS computer_manufacturer VARCHAR(255),
ADD COLUMN IF NOT EXISTS computer_system_type VARCHAR(100);
```

### Passo 2: Atualizar o Agente

1. Substitua o arquivo `AGENTE/agente.py` pela versão atualizada
2. Certifique-se de que o módulo `wmi` está instalado (apenas para Windows):
   ```bash
   pip install wmi
   ```

### Passo 3: Testar as Funcionalidades

Execute o script de teste:

```bash
cd SERVER/Ver_0_B
python test_computer_info.py
```

### Passo 4: Verificar a Aplicação

1. Inicie a aplicação Flask:
   ```bash
   python app.py
   ```

2. Faça um check-in do agente para testar a coleta de dados

3. Verifique na interface web se as informações do modelo e fabricante aparecem

## Exemplos de Dados Coletados

### Windows
```json
{
  "computer_model": "Latitude 5520",
  "computer_manufacturer": "Dell Inc.",
  "computer_system_type": "x64-based PC"
}
```

### Linux
```json
{
  "computer_model": "ThinkPad X1 Carbon",
  "computer_manufacturer": "LENOVO",
  "computer_system_type": null
}
```

### macOS
```json
{
  "computer_model": "MacBook Pro",
  "computer_manufacturer": "Apple Inc.",
  "computer_system_type": null
}
```

## Compatibilidade

- **Windows**: Requer módulo `wmi` instalado
- **Linux**: Funciona com sistemas que têm DMI disponível
- **macOS**: Usa comandos nativos do sistema
- **Banco de Dados**: PostgreSQL (testado com versão 12+)

## Troubleshooting

### Erro: "wmi module not found"
```bash
pip install wmi
```

### Erro: "Permission denied" no Linux
O usuário precisa ter acesso de leitura aos arquivos DMI:
```bash
sudo chmod 644 /sys/class/dmi/id/*
```

### Colunas não aparecem no banco
Execute manualmente o script SQL:
```sql
ALTER TABLE assets 
ADD COLUMN IF NOT EXISTS computer_model VARCHAR(255),
ADD COLUMN IF NOT EXISTS computer_manufacturer VARCHAR(255),
ADD COLUMN IF NOT EXISTS computer_system_type VARCHAR(100);
```

## Benefícios

1. **Inventário Mais Completo**: Informações detalhadas do hardware
2. **Identificação de Equipamentos**: Facilita a identificação de modelos específicos
3. **Suporte Técnico**: Ajuda no diagnóstico de problemas por modelo
4. **Gestão de Ativos**: Melhor controle sobre os equipamentos da organização
5. **Relatórios**: Possibilidade de gerar relatórios por fabricante/modelo

## Próximos Passos

1. Atualizar a interface web para exibir as novas informações
2. Adicionar filtros por fabricante/modelo
3. Criar relatórios específicos por tipo de equipamento
4. Implementar alertas para equipamentos de fabricantes específicos 
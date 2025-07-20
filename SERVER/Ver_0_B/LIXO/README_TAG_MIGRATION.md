# Migração da Coluna "Tag" na Tabela Assets

## Resumo das Alterações

Foi adicionada uma nova coluna `tag` na tabela `assets` para armazenar a tag do asset enviada pelo agente. Esta tag é obtida através do SerialNumber da BIOS do equipamento.

## Arquivos Modificados

### 1. `models/database.py`
- Adicionada coluna `tag = db.Column(db.String(255))` no modelo `Asset`
- Esta coluna irá armazenar a tag obtida pelo agente

### 2. `models/database_schema.sql`
- Adicionada coluna `tag VARCHAR(255)` na definição da tabela `assets`
- Atualizado o esquema do banco de dados

### 3. `routes/rotas_agente/rt_agente_checkin.py`
- Modificado para processar a informação `tag` do `system_info` enviada pelo agente
- Adicionado `tag=system_info.get('tag')` na criação de novos assets
- Adicionado `'tag': system_info.get('tag')` no dicionário de campos a serem atualizados

### 4. `templates/asset_detail.html`
- **Observação**: O template já estava exibindo a tag na linha 32:
  ```html
  <p><strong>Tag:</strong> {{ asset.tag }}</p>
  ```

## Como Executar a Migração

### 1. Backup do Banco de Dados
Antes de executar a migração, faça backup do banco de dados:
```bash
pg_dump -h 127.0.0.1 -U isac -d DB_ASSETS > backup_antes_tag_migration.sql
```

### 2. Executar o Script de Migração
Execute o script SQL para adicionar a coluna:
```bash
psql -h 127.0.0.1 -U isac -d DB_ASSETS -f LIXO/add_tag_column.sql
```

### 3. Verificar a Migração
Verifique se a coluna foi adicionada corretamente:
```sql
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'assets' AND column_name = 'tag';
```

### 4. Reiniciar o Servidor
Após a migração, reinicie o servidor Flask para carregar as alterações do modelo:
```bash
python app.py
```

## Funcionamento

1. **Coleta no Agente**: O agente coleta a tag através do método `get_tag_asset()` que executa:
   ```powershell
   Get-WmiObject Win32_BIOS | Select-Object SerialNumber
   ```

2. **Envio para Servidor**: A tag é incluída no `system_info` e enviada no pacote de check-in

3. **Processamento no Servidor**: O servidor processa a tag e armazena na coluna `tag` da tabela `assets`

4. **Exibição na Interface**: A tag é exibida na página de detalhes do asset

## Observações

- A coluna `tag` pode ser NULL, pois nem todos os equipamentos podem ter uma tag válida
- A tag é diferente do `asset_tag` que é usado como identificador único
- O campo `tag` armazena especificamente o SerialNumber da BIOS obtido pelo agente

## Rollback (se necessário)

Para reverter a migração, execute:
```sql
ALTER TABLE assets DROP COLUMN tag;
``` 
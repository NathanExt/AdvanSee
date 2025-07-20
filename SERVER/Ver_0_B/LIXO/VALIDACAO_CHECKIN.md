# Guia de Validação: Checkin Agente VER_2

## 🎯 Objetivo

Este guia ajuda a validar se o agente VER_2 está enviando dados corretamente e se o servidor Ver_0_B está processando e salvando o software instalado adequadamente.

## ✅ Checklist de Validação

### 1. Verificar Logs do Servidor

**Localização**: `logs/` (diretório do servidor)

**O que procurar**:
```
INFO - Realizando check-in para ativo [UUID]
INFO - Check-in realizado com sucesso: 200
```

**Erros a evitar**:
```
ERROR - Erro no check-in: 400/500
WARNING - Asset tag/UUID não encontrado
```

### 2. Validar Banco de Dados

**Conectar ao PostgreSQL**:
```bash
psql -h 127.0.0.1 -U isac -d DB_ASSETS
```

**Verificar assets criados**:
```sql
-- Verificar se o asset foi criado/atualizado
SELECT asset_tag, tag, name, last_seen, created_at 
FROM assets 
WHERE asset_tag LIKE 'TEST-%' 
ORDER BY created_at DESC 
LIMIT 5;
```

**Verificar software instalado**:
```sql
-- Verificar software instalado nos assets de teste
SELECT a.asset_tag, a.name as asset_name, 
       s.name as software_name, s.version, s.vendor, s.created_at
FROM assets a
JOIN installed_software s ON a.id = s.asset_id
WHERE a.asset_tag LIKE 'TEST-%'
ORDER BY s.created_at DESC
LIMIT 10;
```

**Contar software por asset**:
```sql
-- Contar quantos softwares foram salvos por asset
SELECT a.asset_tag, a.name, COUNT(s.id) as software_count
FROM assets a
LEFT JOIN installed_software s ON a.id = s.asset_id
WHERE a.asset_tag LIKE 'TEST-%'
GROUP BY a.id, a.asset_tag, a.name;
```

### 3. Testar Interface Web

**Acessar a página de software**:
1. Abrir navegador: `http://127.0.0.1:5000/software`
2. Verificar estatísticas atualizadas
3. Buscar por software de teste (ex: "Microsoft Office")
4. Validar que Asset IDs aparecem corretamente

**Verificar gráficos**:
- Top 10 software deve incluir itens de teste
- Top 10 fabricantes deve mostrar "Microsoft Corporation", "Google LLC", etc.

### 4. Executar Script de Teste

**Executar o script de compatibilidade**:
```bash
cd SERVER/Ver_0_B
python test_compatibility.py
```

**Resultado esperado**:
```
🚀 INICIANDO TESTES DE COMPATIBILIDADE
==================================================
TESTE: AGENTE VER_1 (Chaves Capitalizadas)
==================================================
Enviando checkin para: TEST-VER1-001
Software instalado: 3 itens
✅ SUCESSO: Checkin processado com sucesso

==================================================
TESTE: AGENTE VER_2 (Chaves Minúsculas)
==================================================
Enviando checkin para: TEST-VER2-002
Software instalado: 3 itens
✅ SUCESSO: Checkin processado com sucesso

==================================================
TESTE: DADOS MISTOS (Teste de Robustez)
==================================================
Enviando checkin para: TEST-MIXED-003
Software instalado: 3 itens
✅ SUCESSO: Checkin processado com sucesso

🏁 TESTES CONCLUÍDOS
```

## 🔍 Problemas Comuns e Soluções

### Problema 1: Asset não criado
**Sintoma**: SQL retorna 0 linhas para assets
**Causa**: UUID/asset_tag inválido ou erro na organização
**Solução**: Verificar logs e confirmar organização no banco

### Problema 2: Software não salvo
**Sintoma**: `software_count = 0` na query
**Causa possível**: Formato de dados ainda incompatível
**Solução**: Verificar se chaves estão sendo processadas corretamente

### Problema 3: Erro 400/500 no checkin
**Sintoma**: Script de teste retorna erro HTTP
**Causa**: Dados malformados ou servidor offline
**Solução**: Verificar formato JSON e status do servidor

## 📊 Métricas de Sucesso

### ✅ Critérios de Aprovação

1. **Assets Criados**: Todos os 3 assets de teste devem aparecer na tabela `assets`
2. **Software Salvo**: Cada asset deve ter 3 itens de software instalado
3. **Formatos Aceitos**: Tanto chaves capitalizadas quanto minúsculas funcionam
4. **Interface Atualizada**: Página /software mostra dados de teste
5. **Logs Limpos**: Sem erros críticos nos logs do servidor

### 📈 Dados Esperados

Após execução dos testes, deve haver:
- **3 assets** com tags: `TEST-VER1-001`, `TEST-VER2-002`, `TEST-MIXED-003`
- **9 registros** na tabela `installed_software` (3 por asset)
- **Software variado**: Microsoft Office, Google Chrome, Firefox, VLC, etc.

## 🚀 Teste com Agente Real

### Preparação
1. Deploy do agente VER_2 em uma máquina de teste
2. Configurar para apontar para o servidor Ver_0_B
3. Executar checkin manual ou aguardar checkin automático

### Validação
1. Verificar logs de checkin
2. Confirmar criação/atualização do asset
3. Validar que software real foi detectado e salvo
4. Testar funcionalidades de busca na interface

## 📝 Relatório de Teste

**Data do Teste**: _____________
**Versão do Servidor**: Ver_0_B
**Versão do Agente**: VER_2

| Teste | Status | Observações |
|-------|---------|-------------|
| Script de Compatibilidade | ⬜ Pass / ⬜ Fail | |
| Assets Criados | ⬜ Pass / ⬜ Fail | |
| Software Salvo | ⬜ Pass / ⬜ Fail | |
| Interface Atualizada | ⬜ Pass / ⬜ Fail | |
| Agente Real | ⬜ Pass / ⬜ Fail | |

**Conclusão**: 
⬜ **APROVADO** - Compatibilidade confirmada
⬜ **REPROVADO** - Requer correções adicionais

---

**💡 Lembre-se**: Este processo garante que a migração do agente VER_1 para VER_2 seja segura e que ambas as versões possam coexistir durante o período de transição. 
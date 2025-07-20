# Dados Padrão - AdvanSee

## Resumo

Este documento descreve os dados padrão que são criados automaticamente no banco de dados AdvanSee para facilitar o início do uso do sistema.

## Dados Criados

### 1. Organização Padrão

**Nome:** AdvanSee Corporation  
**Descrição:** Organização padrão do sistema AdvanSee - Sistema de Gestão de Inventário Automatizado  
**ID:** 1

### 2. Usuário Administrador

**Username:** admin  
**Email:** admin@advansee.com  
**Senha:** admin123  
**Nome:** Administrador Sistema  
**Role:** admin  
**Status:** Ativo

⚠️ **IMPORTANTE:** Altere a senha do usuário admin após o primeiro login!

### 3. Categorias de Ativos

#### Categorias Principais
- **Computadores** - Desktops, notebooks e workstations
- **Servidores** - Servidores físicos e virtuais
- **Redes** - Switches, roteadores, firewalls
- **Periféricos** - Impressoras, scanners, monitores
- **Software** - Licenças de software
- **Móveis** - Móveis e mobiliário corporativo
- **Equipamentos de TI** - Outros equipamentos de tecnologia

#### Subcategorias

**Computadores:**
- Desktop
- Notebook
- Workstation
- Tablet

**Redes:**
- Switch
- Roteador
- Firewall
- Access Point

**Periféricos:**
- Impressora
- Scanner
- Monitor
- Teclado/Mouse

### 4. Fornecedores Padrão

| Fornecedor | Email | Telefone | Website |
|------------|-------|----------|---------|
| Dell Technologies | contato@dell.com | +55 11 4004-4000 | dell.com |
| Lenovo | contato@lenovo.com | +55 11 4003-3000 | lenovo.com |
| HP Inc. | contato@hp.com | +55 11 4002-2000 | hp.com |
| Microsoft | contato@microsoft.com | +55 11 4001-1000 | microsoft.com |
| Cisco Systems | contato@cisco.com | +55 11 4000-0000 | cisco.com |
| Samsung | contato@samsung.com | +55 11 4005-5000 | samsung.com |
| Apple Inc. | contato@apple.com | +55 11 4006-6000 | apple.com |

### 5. Localizações Padrão

| Nome | Endereço | Edifício | Andares |
|------|----------|----------|---------|
| Matriz - São Paulo | Av. Paulista, 1000 - São Paulo, SP | Edifício Matriz | 1º ao 10º |
| Filial - Rio de Janeiro | Av. Rio Branco, 100 - Rio de Janeiro, RJ | Edifício Filial RJ | 1º ao 5º |
| Filial - Belo Horizonte | Av. Afonso Pena, 200 - Belo Horizonte, MG | Edifício Filial BH | 1º ao 3º |
| Data Center - São Paulo | Av. Engenheiro Caetano Álvares, 500 - São Paulo, SP | Data Center Principal | Térreo e Subsolo |

## Como Criar os Dados Padrão

### Opção 1: Script Python (Recomendado)

```bash
cd SERVER/Ver_0_B
python create_default_data.py
```

### Opção 2: Script SQL

```bash
# Conectar ao PostgreSQL
psql -U isac -d ISAC_BD_ADVANSEE_2 -f insert_default_organization.sql
```

### Opção 3: Manual via Interface Web

1. Acesse o sistema: `http://localhost:5000`
2. Faça login com: `admin` / `admin123`
3. Vá para "Organizations" e crie uma nova organização
4. Vá para "Users" e crie novos usuários
5. Vá para "Categories" e crie categorias de ativos
6. Vá para "Vendors" e crie fornecedores
7. Vá para "Locations" e crie localizações

## Personalização

### Alterar Nome da Organização

```sql
UPDATE organizations 
SET name = 'Sua Empresa Ltda', 
    description = 'Descrição da sua empresa'
WHERE id = 1;
```

### Alterar Senha do Admin

```sql
-- Nova senha: nova_senha123
UPDATE users 
SET password_hash = 'hash_da_nova_senha'
WHERE username = 'admin';
```

### Adicionar Novos Usuários

```sql
INSERT INTO users (organization_id, username, email, password_hash, first_name, last_name, role, is_active)
VALUES (
    1, -- ID da organização
    'usuario1',
    'usuario1@empresa.com',
    'hash_da_senha',
    'Nome',
    'Sobrenome',
    'user',
    true
);
```

## Estrutura Hierárquica das Categorias

```
Computadores
├── Desktop
├── Notebook
├── Workstation
└── Tablet

Redes
├── Switch
├── Roteador
├── Firewall
└── Access Point

Periféricos
├── Impressora
├── Scanner
├── Monitor
└── Teclado/Mouse
```

## Benefícios dos Dados Padrão

1. **Início Rápido:** Sistema pronto para uso imediato
2. **Estrutura Organizada:** Categorias e fornecedores comuns já configurados
3. **Exemplo Prático:** Demonstra como organizar ativos
4. **Base para Expansão:** Facilita adição de novos dados
5. **Padronização:** Estrutura consistente para diferentes organizações

## Próximos Passos

1. **Alterar Senha:** Mude a senha do usuário admin
2. **Personalizar:** Ajuste os dados para sua organização
3. **Adicionar Usuários:** Crie contas para sua equipe
4. **Configurar Agentes:** Instale e configure os agentes nos computadores
5. **Importar Ativos:** Adicione seus ativos existentes

## Troubleshooting

### Erro: "Organização já existe"
- O script verifica se os dados já existem antes de criar
- Pode ser executado múltiplas vezes sem problemas

### Erro: "Usuário admin já existe"
- O usuário admin já foi criado anteriormente
- Use as credenciais existentes ou altere a senha

### Erro: "Categoria duplicada"
- As categorias já existem no banco
- Pode continuar usando as categorias existentes

## Suporte

Para dúvidas sobre os dados padrão:
1. Verifique os logs do script
2. Consulte a documentação do sistema
3. Execute o script novamente se necessário
4. Verifique as permissões do banco de dados 
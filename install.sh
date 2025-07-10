#!/bin/bash

echo "========================================"
echo "AdvanSee - Instalação Automatizada"
echo "========================================"
echo

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python3 não encontrado!"
    echo "Por favor, instale o Python 3.8+ e tente novamente."
    exit 1
fi

echo "Python encontrado!"
python3 --version
echo

# Criar ambiente virtual se não existir
if [ ! -d "venv_advansee" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv_advansee
    if [ $? -ne 0 ]; then
        echo "ERRO: Falha ao criar ambiente virtual!"
        exit 1
    fi
    echo "Ambiente virtual criado com sucesso!"
else
    echo "Ambiente virtual já existe."
fi

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source venv_advansee/bin/activate

# Atualizar pip
echo "Atualizando pip..."
python -m pip install --upgrade pip

# Instalar dependências do servidor
echo
echo "Instalando dependências do servidor..."
cd SERVER/Ver_0_B
pip install -r requirements-minimal.txt
if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao instalar dependências do servidor!"
    exit 1
fi

# Voltar para o diretório raiz
cd ../..

# Instalar dependências do agente
echo
echo "Instalando dependências do agente..."
cd AGENTE
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao instalar dependências do agente!"
    exit 1
fi

# Voltar para o diretório raiz
cd ..

echo
echo "========================================"
echo "Instalação concluída com sucesso!"
echo "========================================"
echo
echo "Para iniciar o servidor:"
echo "  1. Ative o ambiente virtual: source venv_advansee/bin/activate"
echo "  2. Vá para SERVER/Ver_0_B"
echo "  3. Execute: python app.py"
echo
echo "Para executar o agente:"
echo "  1. Ative o ambiente virtual: source venv_advansee/bin/activate"
echo "  2. Vá para AGENTE"
echo "  3. Execute: python agente.py"
echo
echo "Consulte o README_INSTALACAO.md para mais detalhes."
echo 
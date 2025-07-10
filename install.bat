@echo off
echo ========================================
echo AdvanSee - Instalacao Automatizada
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale o Python 3.8+ e tente novamente.
    pause
    exit /b 1
)

echo Python encontrado!
python --version
echo.

REM Criar ambiente virtual se não existir
if not exist "venv_advansee" (
    echo Criando ambiente virtual...
    python -m venv venv_advansee
    if errorlevel 1 (
        echo ERRO: Falha ao criar ambiente virtual!
        pause
        exit /b 1
    )
    echo Ambiente virtual criado com sucesso!
) else (
    echo Ambiente virtual ja existe.
)

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv_advansee\Scripts\activate.bat

REM Atualizar pip
echo Atualizando pip...
python -m pip install --upgrade pip

REM Instalar dependências do servidor
echo.
echo Instalando dependencias do servidor...
cd SERVER\Ver_0_B
pip install -r requirements-minimal.txt
if errorlevel 1 (
    echo ERRO: Falha ao instalar dependencias do servidor!
    pause
    exit /b 1
)

REM Voltar para o diretório raiz
cd ..\..

REM Instalar dependências do agente
echo.
echo Instalando dependencias do agente...
cd AGENTE
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRO: Falha ao instalar dependencias do agente!
    pause
    exit /b 1
)

REM Voltar para o diretório raiz
cd ..

echo.
echo ========================================
echo Instalacao concluida com sucesso!
echo ========================================
echo.
echo Para iniciar o servidor:
echo   1. Ative o ambiente virtual: venv_advansee\Scripts\activate.bat
echo   2. Vá para SERVER\Ver_0_B
echo   3. Execute: python app.py
echo.
echo Para executar o agente:
echo   1. Ative o ambiente virtual: venv_advansee\Scripts\activate.bat
echo   2. Vá para AGENTE
echo   3. Execute: python agente.py
echo.
echo Consulte o README_INSTALACAO.md para mais detalhes.
echo.
pause 
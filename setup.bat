@echo off
echo ============================================
echo  Futuro Digital LatAm - Pipeline Setup
echo ============================================
echo.

:: Check Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado.
    echo Descargalo desde https://www.python.org/downloads/
    echo Asegurate de marcar "Add Python to PATH" al instalar.
    pause
    exit /b 1
)

echo [OK] Python encontrado:
python --version
echo.

:: Create virtual environment (skip if already exists)
echo [1/3] Creando entorno virtual...
if exist venv\Scripts\activate.bat (
    echo [OK] Entorno virtual ya existe, omitiendo creacion.
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] No se pudo crear el entorno virtual.
        pause
        exit /b 1
    )
    echo [OK] Entorno virtual creado.
)
echo.

:: Install dependencies
echo [2/3] Instalando dependencias...
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] No se pudieron instalar las dependencias.
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas.
echo.

:: Verify key libraries
echo [3/3] Verificando instalacion...
python -c "import pandas, matplotlib, scipy, numpy; print('[OK] pandas', pandas.__version__); print('[OK] matplotlib', matplotlib.__version__); print('[OK] scipy', scipy.__version__); print('[OK] numpy', numpy.__version__)"
echo.

echo ============================================
echo  Setup completo. Puedes abrir Claude Code
echo  en esta carpeta y escribir "corre todo".
echo ============================================
pause

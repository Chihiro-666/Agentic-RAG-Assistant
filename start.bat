@echo off
setlocal enabledelayedexpansion

:: Change to repository root
cd /d "%~dp0"

echo ==========================================
echo   Starting Agentic RAG System
echo ==========================================

:: 1. Check and prepare the environment file
if not exist "project\.env" (
    if exist "project\.env.example" (
        echo Creating project\.env from project\.env.example...
        copy "project\.env.example" "project\.env" >nul
    )
)

:: 2. Check Ollama service
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Ollama is not running at localhost:11434.
    echo           Start Ollama before using the local model.
)

:: 3. Download the configured model on first launch if Ollama has no models
if not defined OLLAMA_MODEL (
    set "OLLAMA_MODEL=llama3.1:8b"
    if exist "project\.env" (
        for /f "usebackq tokens=1,* delims==" %%A in ("project\.env") do (
            if "%%A"=="OLLAMA_MODEL" set "OLLAMA_MODEL=%%B"
        )
    )
)
where ollama >nul 2>&1
if %errorlevel% equ 0 (
    set "FOUND_OLLAMA_MODEL="
    for /f "skip=1 tokens=1" %%M in ('ollama list 2^>nul') do (
        if not defined FOUND_OLLAMA_MODEL set "FOUND_OLLAMA_MODEL=%%M"
    )
    if not defined FOUND_OLLAMA_MODEL (
        curl -s http://localhost:11434/api/tags >nul 2>&1
        if !errorlevel! equ 0 (
            echo No Ollama models found. Downloading %OLLAMA_MODEL%...
            ollama pull %OLLAMA_MODEL%
            if errorlevel 1 (
                echo [ERROR] Could not download %OLLAMA_MODEL%. Check network and Ollama, then run:
                echo         ollama pull %OLLAMA_MODEL%
                pause
                exit /b 1
            )
        )
    )
)

:: 4. Start the application (prefer uv)
where uv >nul 2>&1
if %errorlevel% equ 0 (
    echo Using uv for Python environment management...
    uv run project\app.py
    if errorlevel 1 goto :app_failed
    goto :end
)

echo uv not found. Using a standard Python virtual environment...

:: Find Python executable (try py, then python)
set "PYTHON_CMD="
where py >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=py"
) else (
    where python >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON_CMD=python"
    )
)

if "%PYTHON_CMD%"=="" (
    echo [ERROR] Python 3.11+ is required, but py or python was not found in PATH.
    pause
    exit /b 1
)

:: Create virtual environment if it does not exist
if not exist ".venv" (
    echo Creating virtual environment in .venv...
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 goto :setup_failed
)

:: Activate virtual environment
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

echo Checking and installing dependencies...
pip install -q -r requirements.txt
if errorlevel 1 goto :setup_failed

echo Starting application...
python project\app.py
if errorlevel 1 goto :app_failed
goto :end

:setup_failed
echo [ERROR] Python environment setup failed. Check your Python installation and network.
pause
exit /b 1

:app_failed
echo.
echo [ERROR] Application startup failed. Review the error above. Press any key to close.
pause
exit /b 1

:end
endlocal

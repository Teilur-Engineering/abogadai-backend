@echo off
echo ========================================
echo Iniciando Backend de Abogadai
echo ========================================
echo.

REM Activar entorno virtual
call venv\Scripts\activate

REM Ejecutar servidor
echo Servidor corriendo en: http://localhost:8000
echo Documentacion API: http://localhost:8000/docs
echo.
uvicorn app.main:app --reload --port 8000

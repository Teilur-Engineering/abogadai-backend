@echo off
echo ========================================
echo Configuracion de Abogadai Backend
echo ========================================
echo.

echo Paso 1: Instalando dependencias Python...
python -m pip install -r requirements.txt

echo.
echo Paso 2: Configuracion completa!
echo.
echo Para ejecutar el servidor:
echo     uvicorn app.main:app --reload --port 8000
echo.
echo Documentacion API:
echo     http://localhost:8000/docs
echo.
echo IMPORTANTE: Asegurate de tener PostgreSQL corriendo
echo y que la base de datos 'abogadai_db' este creada.
echo.
pause

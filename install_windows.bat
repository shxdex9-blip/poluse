@echo off
chcp 65001 >nul
cd /d "%~dp0"
py -3.11 -m venv .venv
if errorlevel 1 py -3 -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if not exist .env copy .env.example .env
echo.
echo Установка завершена. Откройте .env и заполните BOT_TOKEN и ADMIN_ID.
pause

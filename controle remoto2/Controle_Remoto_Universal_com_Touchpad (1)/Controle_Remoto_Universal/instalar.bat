@echo off
chcp 65001 >nul
title Instalar Controle Remoto Universal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Python 3 nao foi encontrado. Instale-o em https://www.python.org/downloads/windows/
  echo Durante a instalacao, marque "Add python.exe to PATH".
  pause
  exit /b 1
)
py -m venv .venv
if errorlevel 1 goto erro
call .venv\Scripts\activate.bat
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
if errorlevel 1 goto erro
echo.
echo Instalacao concluida. Execute iniciar.bat.
pause
exit /b 0
:erro
echo.
echo A instalacao falhou. Verifique a ligacao a Internet e a instalacao do Python.
pause
exit /b 1

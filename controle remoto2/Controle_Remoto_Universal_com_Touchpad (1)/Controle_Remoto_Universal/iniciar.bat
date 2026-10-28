@echo off
chcp 65001 >nul
title Controle Remoto Universal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Execute instalar.bat primeiro.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" app.py
pause

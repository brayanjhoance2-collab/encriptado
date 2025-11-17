@echo off
chcp 65001 > nul
cd /d "%~dp0"
python_portable\python.exe launcher.py
pause

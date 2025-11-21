@echo off
chcp 65001 > nul
cd /d "%~dp0"
lib4710\pythonw.exe launcher.py

@echo off
setlocal

:: Stelle sicher, dass Python installiert ist
where python >nul 2>nul
if errorlevel 1 (
    echo [*] Python ist nicht installiert. Lade den Installer herunter...
    curl -o python_installer.exe https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    if errorlevel 1 (
        echo [!] Fehler bei der Python-Installation.
        exit /b 1
    )
    echo [*] Python wurde erfolgreich installiert.
)

:: Installiere benötigte Module mit pip
echo [*] Installiere benötigte Python-Module...
python -m pip install --upgrade pip
python -m pip install requests pyinstaller

:: Erstelle das Python-Skript mit den gewünschten Imports
echo [*] Erstelle test_script.py...
echo import os> test_script.py
echo import time>> test_script.py
echo import requests>> test_script.py
echo import random>> test_script.py
echo import string>> test_script.py
echo import datetime>> test_script.py
echo import shutil>> test_script.py
echo import tempfile>> test_script.py
echo import PyInstaller.__main__>> test_script.py
echo import subprocess>> test_script.py
echo import sys>> test_script.py
echo import webbrowser>> test_script.py
echo print("Alle Module erfolgreich importiert.")>> test_script.py
echo imput()

:: Führe das Skript aus
echo [*] Starte test_script.py...
python test_script.py

endlocal
pause

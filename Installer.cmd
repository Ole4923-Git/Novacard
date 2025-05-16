@echo off
setlocal

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

python -m pip install requests pyinstaller
cls
NovaCard.py
exit

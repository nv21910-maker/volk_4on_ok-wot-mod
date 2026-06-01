@echo off
REM Volk_4on_ok WoT Toolkit - Windows Installer
REM For Windows 10/11

echo.
echo ============================================================
echo    VOLK_4ON_OK WOT TOOLKIT v2.0 - Windows Installer
echo ============================================================
echo.

REM Check Python version
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8+ from python.org
    echo.
    pause
    exit /b 1
)

echo [1/4] Checking Python version...
python --version
echo.

echo [2/4] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo.

echo [3/4] Creating shortcuts...
echo @echo off > volk_toolkit.bat
echo python "%%~dp0volk_wot_toolkit.py" %%%%* >> volk_toolkit.bat
echo @echo off > volk_mod.bat
echo python "%%~dp0volk_4on_ok_mod.py" %%%%* >> volk_mod.bat
echo @echo off > volk_jokes.bat
echo python "%%~dp0random_joke_generator.py" %%%%* >> volk_jokes.bat
echo.

echo [4/4] Testing installation...
python volk_wot_toolkit.py >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Installation may have issues
) else (
    echo.
)

echo ============================================================
echo    INSTALLATION COMPLETE!
echo ============================================================
echo.
echo Quick Start:
echo   • volk_toolkit.bat         - Run WoT Toolkit
echo   • volk_mod.bat             - Run WoT Mod
echo   • volk_jokes.bat           - Run Joke Generator
echo.
echo Or use command line:
echo   python volk_wot_toolkit.py interactive
echo   python volk_4on_ok_mod.py
echo   python random_joke_generator.py interactive
echo.
echo Documentation: README.md
echo.
pause

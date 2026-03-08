@echo off
REM ============================================================
REM SpectrumTek Commissions Converter - Windows Build Script
REM ============================================================
REM This script builds both the portable .exe and installer package.
REM
REM Prerequisites:
REM   1. Python 3.8+ installed and in PATH
REM   2. pip install pyinstaller openpyxl
REM   3. Inno Setup 6.x installed (for installer build)
REM
REM Usage: Run this script from the project root directory
REM        > cd Commissions-XML-To-XLS
REM        > build\build_windows.bat
REM ============================================================

echo.
echo ========================================
echo SpectrumTek Commissions Converter Build
echo ========================================
echo.

REM Change to project root directory
cd /d "%~dp0\.."
set PROJECT_ROOT=%CD%
echo Project root: %PROJECT_ROOT%
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    echo Please install Python 3.8+ and add it to PATH
    pause
    exit /b 1
)

REM Install/upgrade dependencies
echo Installing dependencies...
pip install --upgrade pyinstaller openpyxl
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist dist rmdir /s /q dist
if exist build\dist rmdir /s /q build\dist
if exist __pycache__ rmdir /s /q __pycache__
if exist sap_commissions_xml\__pycache__ rmdir /s /q sap_commissions_xml\__pycache__
echo.

REM Build portable version
echo.
echo ========================================
echo Building Portable Version (Single EXE)
echo ========================================
echo.
pyinstaller build\spectrumtek_portable.spec --clean --noconfirm
if errorlevel 1 (
    echo ERROR: Portable build failed
    pause
    exit /b 1
)
echo Portable build complete: dist\SpectrumTek_Commissions_Converter.exe
echo.

REM Rename portable exe
move dist\SpectrumTek_Commissions_Converter.exe dist\SpectrumTek_Commissions_Converter_Portable.exe

REM Build installer version
echo.
echo ========================================
echo Building Installer Version (Directory)
echo ========================================
echo.
pyinstaller build\spectrumtek_installer.spec --clean --noconfirm
if errorlevel 1 (
    echo ERROR: Installer build failed
    pause
    exit /b 1
)
echo Installer build complete: dist\SpectrumTek_Commissions_Converter\
echo.

REM Check for Inno Setup
REM Try common installation paths
set ISCC_PATH=
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set ISCC_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
)
if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set ISCC_PATH=C:\Program Files\Inno Setup 6\ISCC.exe
)

if "%ISCC_PATH%"=="" (
    echo.
    echo WARNING: Inno Setup not found.
    echo To build the installer, please:
    echo   1. Download Inno Setup from: https://jrsoftware.org/isinfo.php
    echo   2. Install it
    echo   3. Run: "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" build\installer.iss
    echo.
) else (
    echo.
    echo ========================================
    echo Building Windows Installer
    echo ========================================
    echo.
    mkdir dist\installer 2>nul
    "%ISCC_PATH%" build\installer.iss
    if errorlevel 1 (
        echo ERROR: Installer build failed
        pause
        exit /b 1
    )
    echo Installer build complete!
    echo.
)

echo.
echo ========================================
echo BUILD COMPLETE
echo ========================================
echo.
echo Output files:
if exist dist\SpectrumTek_Commissions_Converter_Portable.exe (
    echo   [PORTABLE] dist\SpectrumTek_Commissions_Converter_Portable.exe
)
if exist dist\SpectrumTek_Commissions_Converter (
    echo   [DIR]      dist\SpectrumTek_Commissions_Converter\
)
if exist dist\installer\*.exe (
    for %%f in (dist\installer\*.exe) do echo   [SETUP]    %%f
)
echo.
pause

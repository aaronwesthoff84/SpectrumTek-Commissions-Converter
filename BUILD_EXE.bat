@echo off
setlocal enabledelayedexpansion

REM ============================================================
REM   SpectrumTek Commissions Converter - Easy EXE Builder
REM   Just double-click this file to build your portable .exe!
REM ============================================================

title SpectrumTek Commissions Converter - EXE Builder

REM Set colors for better readability
color 0A

echo.
echo  ============================================================
echo  =                                                          =
echo  =     SpectrumTek Commissions Converter - EXE Builder      =
echo  =                                                          =
echo  ============================================================
echo.
echo  This script will automatically build a portable .exe file
echo  of the SpectrumTek Commissions XML-to-Excel Converter.
echo.
echo  The portable .exe is a single file that runs on any Windows
echo  computer - no installation required!
echo.
echo  Press any key to start building, or close this window to cancel.
echo.
pause >nul

REM Change to the directory where this script is located
cd /d "%~dp0"
set PROJECT_ROOT=%CD%

echo.
echo  [Step 1/5] Checking Python installation...
echo  ------------------------------------------

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo  ERROR: Python is not installed or not in your PATH!
    echo.
    echo  To fix this:
    echo    1. Download Python from: https://www.python.org/downloads/
    echo    2. During installation, CHECK the box that says:
    echo       "Add Python to PATH"
    echo    3. Restart your computer after installation
    echo    4. Run this script again
    echo.
    goto :error_exit
)

REM Display Python version
for /f "tokens=*" %%v in ('python --version 2^>^&1') do set PYTHON_VER=%%v
echo  SUCCESS: %PYTHON_VER% is installed
echo.

echo.
echo  [Step 2/5] Installing required packages...
echo  ------------------------------------------
echo  Installing PyInstaller (this may take a minute)...
echo.

pip install pyinstaller openpyxl --quiet --disable-pip-version-check 2>nul
if errorlevel 1 (
    echo  Trying with --user flag...
    pip install pyinstaller openpyxl --user --quiet --disable-pip-version-check 2>nul
    if errorlevel 1 (
        color 0C
        echo.
        echo  ERROR: Failed to install required packages!
        echo.
        echo  Try running this command manually in Command Prompt:
        echo    pip install pyinstaller openpyxl
        echo.
        goto :error_exit
    )
)
echo  SUCCESS: All required packages are installed
echo.

echo.
echo  [Step 3/5] Cleaning up old builds...
echo  ------------------------------------

if exist "%PROJECT_ROOT%\dist" (
    echo  Removing old dist folder...
    rmdir /s /q "%PROJECT_ROOT%\dist" 2>nul
)
if exist "%PROJECT_ROOT%\build_temp" (
    rmdir /s /q "%PROJECT_ROOT%\build_temp" 2>nul
)

REM Clean Python cache
if exist "%PROJECT_ROOT%\__pycache__" rmdir /s /q "%PROJECT_ROOT%\__pycache__" 2>nul
if exist "%PROJECT_ROOT%\sap_commissions_xml\__pycache__" rmdir /s /q "%PROJECT_ROOT%\sap_commissions_xml\__pycache__" 2>nul

echo  SUCCESS: Cleaned up old files
echo.

echo.
echo  [Step 4/5] Building the portable EXE...
echo  ---------------------------------------
echo  This may take 1-3 minutes. Please be patient...
echo.

REM Run PyInstaller with the spec file
pyinstaller build\spectrumtek_portable.spec --clean --noconfirm --workpath=build_temp --distpath=dist 2>&1

if errorlevel 1 (
    color 0C
    echo.
    echo  ERROR: The build process failed!
    echo.
    echo  Common solutions:
    echo    - Make sure no antivirus is blocking PyInstaller
    echo    - Try running as Administrator
    echo    - Check that all project files are present
    echo.
    goto :error_exit
)

REM Clean up temp build folder
if exist "%PROJECT_ROOT%\build_temp" rmdir /s /q "%PROJECT_ROOT%\build_temp" 2>nul

echo.
echo  [Step 5/5] Verifying the build...
echo  ---------------------------------

if exist "%PROJECT_ROOT%\dist\SpectrumTek_Commissions_Converter.exe" (
    REM Get file size
    for %%A in ("%PROJECT_ROOT%\dist\SpectrumTek_Commissions_Converter.exe") do set EXE_SIZE=%%~zA
    set /a EXE_SIZE_MB=!EXE_SIZE!/1048576
    
    color 0A
    echo.
    echo  ============================================================
    echo  =                                                          =
    echo  =                   BUILD SUCCESSFUL!                      =
    echo  =                                                          =
    echo  ============================================================
    echo.
    echo  Your portable EXE has been created:
    echo.
    echo    Location: %PROJECT_ROOT%\dist\
    echo    Filename: SpectrumTek_Commissions_Converter.exe
    echo    Size:     ~!EXE_SIZE_MB! MB
    echo.
    echo  You can now:
    echo    - Copy this .exe file to any Windows computer
    echo    - Run it directly - no installation needed
    echo    - Share it with your team
    echo.
    echo  ============================================================
    echo.
    
    set /p OPEN_FOLDER="  Would you like to open the output folder? (Y/N): "
    if /i "!OPEN_FOLDER!"=="Y" (
        explorer "%PROJECT_ROOT%\dist"
    )
) else (
    color 0C
    echo.
    echo  ERROR: The .exe file was not created.
    echo  Check the output above for error messages.
    echo.
    goto :error_exit
)

echo.
echo  Press any key to exit...
pause >nul
exit /b 0

:error_exit
echo.
echo  ============================================================
echo  =                     BUILD FAILED                         =
echo  ============================================================
echo.
echo  If you need help, please check the BUILD_GUIDE.md file
echo  or contact SpectrumTek support.
echo.
echo  Press any key to exit...
pause >nul
exit /b 1

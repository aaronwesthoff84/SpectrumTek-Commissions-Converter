# SpectrumTek Commissions Converter - Build Guide

This guide explains how to build distributable packages for the SpectrumTek Commissions Converter application.

## Overview

The build process creates two distribution options:

1. **Portable Version**: A single `.exe` file that can run without installation
2. **Installer Version**: A Windows Setup installer (`.exe`) that installs the application to Program Files

---

## Prerequisites

### Required Software

1. **Python 3.8+** 
   - Download from: https://python.org/downloads/
   - Ensure "Add Python to PATH" is checked during installation

2. **Python Packages**
   ```bash
   pip install pyinstaller openpyxl
   ```

3. **Inno Setup 6** (for creating the Windows installer)
   - Download from: https://jrsoftware.org/isinfo.php
   - Install to the default location

### Optional

- **Application Icon** (`assets/icon.ico`): A 256x256 .ico file for the application
- **Installer Images**: Custom banner/icon images for the installer wizard

---

## Quick Build (Automated)

Run the build script from the project root:

```batch
cd Commissions-XML-To-XLS
build\build_windows.bat
```

This will:
1. Install/update dependencies
2. Build the portable single-file `.exe`
3. Build the directory version for the installer
4. Build the Windows installer (if Inno Setup is installed)

---

## Manual Build Steps

### Step 1: Build the Portable Version

The portable version is a single `.exe` file containing everything needed.

```bash
cd Commissions-XML-To-XLS
pyinstaller build/spectrumtek_portable.spec --clean --noconfirm
```

**Output**: `dist/SpectrumTek_Commissions_Converter.exe`

### Step 2: Build the Installer Version

The installer version creates a directory with the executable and dependencies.

```bash
pyinstaller build/spectrumtek_installer.spec --clean --noconfirm
```

**Output**: `dist/SpectrumTek_Commissions_Converter/` (directory)

### Step 3: Create the Windows Installer

Open Inno Setup Compiler and:
1. File → Open → Select `build/installer.iss`
2. Build → Compile

Or from command line:

```batch
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" build\installer.iss
```

**Output**: `dist/installer/SpectrumTek_Commissions_Converter_Setup_1.0.0.exe`

---

## Output Files

After a successful build:

```
dist/
├── SpectrumTek_Commissions_Converter_Portable.exe    # Portable single-file version
├── SpectrumTek_Commissions_Converter/                # Directory build (for installer)
│   ├── SpectrumTek_Commissions_Converter.exe
│   └── ... (support files)
└── installer/
    └── SpectrumTek_Commissions_Converter_Setup_1.0.0.exe  # Windows installer
```

---

## Configuration Files

| File | Purpose |
|------|--------|
| `build/spectrumtek_portable.spec` | PyInstaller config for single-file build |
| `build/spectrumtek_installer.spec` | PyInstaller config for directory build |
| `build/installer.iss` | Inno Setup script for Windows installer |
| `build/version_info.txt` | Windows version info embedded in .exe |
| `build/build_windows.bat` | Automated build script |

---

## Customization

### Changing Version Number

1. Edit `build/version_info.txt` - Update `filevers` and `prodvers`
2. Edit `build/installer.iss` - Update `MyAppVersion` define

### Adding Application Icon

1. Create a 256x256 `.ico` file
2. Save as `assets/icon.ico`
3. The build will automatically use it

### Customizing Installer Appearance

1. Create installer banner (164x314 pixels) and save as `assets/installer_banner.bmp`
2. Create installer icon (55x58 pixels) and save as `assets/installer_icon.bmp`
3. Uncomment the `WizardImageFile` and `WizardSmallImageFile` lines in `build/installer.iss`

---

## Troubleshooting

### "Python not found"
- Ensure Python is installed and added to PATH
- Try running `python --version` to verify

### "ModuleNotFoundError: No module named 'openpyxl'"
- Run: `pip install openpyxl`

### "PyInstaller not found"
- Run: `pip install pyinstaller`

### Antivirus False Positives
PyInstaller-built executables sometimes trigger antivirus warnings. This is a known issue with PyInstaller. Options:
- Sign the executable with a code signing certificate
- Submit the file to your antivirus vendor for whitelisting
- Use the directory build (less likely to trigger alerts)

### Large File Size
The portable version includes all Python dependencies. To reduce size:
- The spec files already exclude unused libraries
- Ensure UPX is available for additional compression

---

## Distribution

### Portable Version
- Simply share the `.exe` file
- Users can run it directly - no installation required
- Works on any Windows 10/11 x64 system

### Installer Version
- Share the `SpectrumTek_Commissions_Converter_Setup_X.X.X.exe` file
- Users run the installer to:
  - Install to Program Files
  - Create Start Menu shortcuts
  - Optionally create Desktop shortcut
  - Enable proper uninstallation via Control Panel

---

## Project Structure

```
Commissions-XML-To-XLS/
├── gui_app.py                    # Main GUI application
├── parse_commissions_xml.py      # CLI entry point
├── requirements.txt              # Python dependencies
├── BUILD_GUIDE.md               # This file
├── sap_commissions_xml/          # Core parser package
│   ├── __init__.py
│   ├── parser.py                 # XML parsing logic
│   ├── writer.py                 # Excel output writer
│   ├── logger.py                 # Logging utilities
│   ├── function_parser.py        # Expression parser
│   └── cli.py                    # CLI interface
├── build/                        # Build configuration
│   ├── spectrumtek_portable.spec # PyInstaller portable config
│   ├── spectrumtek_installer.spec# PyInstaller installer config
│   ├── installer.iss             # Inno Setup script
│   ├── version_info.txt          # Windows version metadata
│   └── build_windows.bat         # Automated build script
└── assets/                       # Application assets
    └── icon.ico                  # Application icon (optional)
```

---

## Support

For issues or questions about the build process, contact SpectrumTek support.

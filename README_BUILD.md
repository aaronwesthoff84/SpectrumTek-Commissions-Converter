# SpectrumTek Commissions Converter - Build Guide

This document provides instructions for building the SpectrumTek Commissions XML-to-Excel Converter for Windows, macOS, and Linux.

---

## 📦 Available Build Packages

| Platform | Package | Contents |
|----------|---------|----------|
| **Windows** | `SpectrumTek_Windows_Build.zip` | Full source + `BUILD_EXE.bat` |
| **macOS** | `SpectrumTek_macOS_Build.zip` | Full source + `BUILD_APP.sh` |
| **Linux** | `SpectrumTek_Linux_Build.zip` | Full source + `BUILD_LINUX.sh` + Pre-built binary |
| **Linux (Binary Only)** | `SpectrumTek_Linux_Binary.zip` | Ready-to-run Linux executable |

---

## 🪟 Windows Build Instructions

### Prerequisites
- Windows 10 or later
- Python 3.8+ (download from [python.org](https://www.python.org/downloads/))
  - **Important:** Check "Add Python to PATH" during installation

### How to Build

1. **Extract** `SpectrumTek_Windows_Build.zip` to any folder
2. **Double-click** `BUILD_EXE.bat`
3. **Wait** for the build to complete (1-3 minutes)
4. **Find** your portable `.exe` in the `dist/` folder

### Output
```
dist/
└── SpectrumTek_Commissions_Converter.exe  (~25 MB)
```

The `.exe` is a single portable file that runs on any Windows computer without installation.

---

## 🍎 macOS Build Instructions

### Prerequisites
- macOS 10.13 (High Sierra) or later
- Python 3.8+ (install via Homebrew or [python.org](https://www.python.org/downloads/))
- Xcode Command Line Tools (run `xcode-select --install` if not installed)

### Installing Python on macOS
```bash
# Option 1: Using Homebrew (recommended)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python3

# Option 2: Download from python.org
# Visit https://www.python.org/downloads/macos/
```

### How to Build

1. **Extract** `SpectrumTek_macOS_Build.zip` to any folder
2. **Open Terminal** and navigate to the extracted folder:
   ```bash
   cd /path/to/extracted/folder
   ```
3. **Make the script executable** (if needed):
   ```bash
   chmod +x BUILD_APP.sh
   ```
4. **Run the build script**:
   ```bash
   ./BUILD_APP.sh
   ```
5. **Wait** for the build to complete (1-3 minutes)
6. **Find** your `.app` bundle in the `dist/` folder

### Output
```
dist/
└── SpectrumTek Commissions Converter.app  (~25 MB)
```

You can:
- Double-click the `.app` to run it
- Drag it to your Applications folder
- Create a `.dmg` for easy distribution

### Code Signing (Optional)
For distribution outside the App Store, you may need to sign the app:
```bash
codesign --force --deep --sign - "dist/SpectrumTek Commissions Converter.app"
```

---

## 🐧 Linux Build Instructions

### Option A: Use the Pre-Built Binary (Easiest)

1. **Extract** `SpectrumTek_Linux_Binary.zip` to any folder
2. **Make executable** (if needed):
   ```bash
   chmod +x SpectrumTek_Commissions_Converter
   ```
3. **Run** the application:
   ```bash
   ./SpectrumTek_Commissions_Converter
   ```

### Option B: Build from Source

#### Prerequisites
- Ubuntu 18.04+ / Debian 10+ / Fedora 32+ (or equivalent)
- Python 3.8+
- tkinter (for GUI support)

#### Installing Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

**Fedora/RHEL:**
```bash
sudo dnf install python3 python3-pip python3-tkinter
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip tk
```

#### How to Build

1. **Extract** `SpectrumTek_Linux_Build.zip` to any folder
2. **Open Terminal** and navigate to the extracted folder:
   ```bash
   cd /path/to/extracted/folder
   ```
3. **Make the script executable** (if needed):
   ```bash
   chmod +x BUILD_LINUX.sh
   ```
4. **Run the build script**:
   ```bash
   ./BUILD_LINUX.sh
   ```
5. **Wait** for the build to complete (1-3 minutes)
6. **Find** your executable in the `dist/` folder

### Output
```
dist/
└── SpectrumTek_Commissions_Converter  (~29 MB)
```

---

## 📁 Project File Structure

```
SpectrumTek_Commissions_Converter/
├── gui_app.py                     # Main GUI application
├── parse_commissions_xml.py       # CLI entry point
├── requirements.txt               # Python dependencies
├── README.md                      # User documentation
├── README_BUILD.md                # This file
│
├── BUILD_EXE.bat                  # Windows build script
├── BUILD_APP.sh                   # macOS build script
├── BUILD_LINUX.sh                 # Linux build script
│
├── build/                         # PyInstaller spec files
│   ├── spectrumtek_portable.spec  # Windows single-file spec
│   ├── spectrumtek_installer.spec # Windows installer spec
│   ├── spectrumtek_macos.spec     # macOS .app bundle spec
│   ├── spectrumtek_linux.spec     # Linux single-file spec
│   └── installer.iss              # Inno Setup script (Windows installer)
│
├── assets/                        # Application icons
│   └── icon.ico                   # Windows icon
│
└── sap_commissions_xml/           # Parser package
    ├── __init__.py
    ├── parser.py
    ├── writer.py
    ├── logger.py
    ├── function_parser.py
    └── cli.py
```

---

## 🎨 Customization

### Application Icon

- **Windows:** Replace `assets/icon.ico` with your icon (256x256 recommended)
- **macOS:** Create `assets/icon.icns` using iconutil or an online converter
- **Linux:** Create `assets/icon.png` (512x512 recommended)

### Version Number

Edit the spec files in `build/` to update version information:
- macOS: Edit `CFBundleShortVersionString` and `CFBundleVersion` in `spectrumtek_macos.spec`
- Windows: Edit `build/version_info.txt` (if present)

---

## 🔧 Troubleshooting

### "Python not found" Error
- Windows: Reinstall Python with "Add to PATH" checked
- macOS/Linux: Use `python3` instead of `python`

### Build Fails with Permission Error
- Windows: Run the build script as Administrator
- macOS/Linux: Try `sudo ./BUILD_*.sh` or check file permissions

### Antivirus Blocking the Executable
PyInstaller executables are sometimes flagged by antivirus. Solutions:
- Add an exception for the `dist/` folder
- Submit a false positive report to your AV vendor

### Missing tkinter on Linux
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

### macOS "App is Damaged" Warning
If macOS shows this warning, run:
```bash
xattr -cr "dist/SpectrumTek Commissions Converter.app"
```

---

## 📧 Support

For build issues or questions, please contact SpectrumTek support or open an issue in the project repository.

---

*SpectrumTek Commissions Converter - Making XML to Excel conversion simple!*

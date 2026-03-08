# SpectrumTek Commissions Converter - Build Guide

This document provides instructions for building the SpectrumTek Commissions XML-to-Excel Converter for Windows, macOS, and Linux.

---

## 📁 Project Structure

```
SpectrumTek-Commissions-Converter/
├── README.md                      # Main readme
├── docs/                          # Documentation
│   └── BUILD_GUIDE.md             # This file
├── source/                        # All source code and build scripts
│   ├── gui_app.py                 # Main GUI application
│   ├── parse_commissions_xml.py   # CLI entry point
│   ├── requirements.txt           # Python dependencies
│   ├── sap_commissions_xml/       # Parser package
│   ├── BUILD_EXE.bat              # Windows build script
│   ├── BUILD_APP.sh               # macOS build script
│   ├── BUILD_LINUX.sh             # Linux build script
│   └── build_config/              # PyInstaller specs & configs
│       ├── spectrumtek_portable.spec
│       ├── spectrumtek_macos.spec
│       ├── spectrumtek_linux.spec
│       ├── spectrumtek_installer.spec
│       ├── installer.iss
│       └── version_info.txt
├── releases/                      # Final executables
│   ├── windows/                   # Windows .exe output
│   ├── macos/                     # macOS .app output
│   └── linux/                     # Linux binary output
└── assets/                        # Application icons
```

---

## 🪟 Windows Build Instructions

### Prerequisites
- Windows 10 or later
- Python 3.8+ (download from [python.org](https://www.python.org/downloads/))
  - **Important:** Check "Add Python to PATH" during installation

### How to Build

1. **Clone or download** the repository
2. **Navigate** to the `source/` folder
3. **Double-click** `BUILD_EXE.bat`
4. **Wait** for the build to complete (1-3 minutes)
5. **Find** your portable `.exe` in `releases/windows/`

### Output
```
releases/windows/
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

1. **Clone or download** the repository
2. **Open Terminal** and navigate to the `source/` folder:
   ```bash
   cd /path/to/SpectrumTek-Commissions-Converter/source
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
6. **Find** your `.app` bundle in `releases/macos/`

### Output
```
releases/macos/
└── SpectrumTek Commissions Converter.app  (~25 MB)
```

You can:
- Double-click the `.app` to run it
- Drag it to your Applications folder
- Create a `.dmg` for easy distribution

### Code Signing (Optional)
For distribution outside the App Store, you may need to sign the app:
```bash
codesign --force --deep --sign - "releases/macos/SpectrumTek Commissions Converter.app"
```

---

## 🐧 Linux Build Instructions

### Prerequisites
- Ubuntu 18.04+ / Debian 10+ / Fedora 32+ (or equivalent)
- Python 3.8+
- tkinter (for GUI support)

### Installing Dependencies

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

### How to Build

1. **Clone or download** the repository
2. **Open Terminal** and navigate to the `source/` folder:
   ```bash
   cd /path/to/SpectrumTek-Commissions-Converter/source
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
6. **Find** your executable in `releases/linux/`

### Output
```
releases/linux/
└── SpectrumTek_Commissions_Converter  (~29 MB)
```

---

## 🎨 Customization

### Application Icon

- **Windows:** Replace `assets/icon.ico` with your icon (256x256 recommended)
- **macOS:** Create `assets/icon.icns` using iconutil or an online converter
- **Linux:** Create `assets/icon.png` (512x512 recommended)

### Version Number

Edit the spec files in `source/build_config/` to update version information:
- macOS: Edit `CFBundleShortVersionString` and `CFBundleVersion` in `spectrumtek_macos.spec`
- Windows: Edit `source/build_config/version_info.txt`

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
- Add an exception for the `releases/` folder
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
xattr -cr "releases/macos/SpectrumTek Commissions Converter.app"
```

---

## 📧 Support

For build issues or questions, please contact SpectrumTek support or open an issue in the project repository.

---

*SpectrumTek Commissions Converter - Making XML to Excel conversion simple!*

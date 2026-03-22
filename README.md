<p><a target="_blank" href="https://app.eraser.io/workspace/67zAsElvi1XJAFC4BPjK" id="edit-in-eraser-github-link"><img alt="Edit in Eraser" src="https://firebasestorage.googleapis.com/v0/b/second-petal-295822.appspot.com/o/images%2Fgithub%2FOpen%20in%20Eraser.svg?alt=media&amp;token=968381c8-a7e7-472a-8ed6-4a6626da5501"></a></p>

#  SpectrumTek Commissions Converter
A GUI application for converting SAP Commissions XML exports to Excel workbooks.

## Project Structure
```
/
├── README.md                    # This file
├── docs/                        # Documentation
│   └── BUILD_GUIDE.md          # Detailed build instructions
├── source/                      # All source code and build scripts
│   ├── gui_app.py              # Main GUI application
│   ├── parse_commissions_xml.py # CLI entry point
│   ├── sap_commissions_xml/    # Parser package
│   ├── requirements.txt        # Python dependencies
│   ├── BUILD_EXE.bat           # Windows build script
│   ├── BUILD_APP.sh            # macOS build script
│   ├── BUILD_LINUX.sh          # Linux build script
│   └── build_config/           # PyInstaller specs & configs
│       ├── spectrumtek_portable.spec
│       ├── spectrumtek_macos.spec
│       ├── spectrumtek_linux.spec
│       ├── spectrumtek_installer.spec
│       ├── installer.iss
│       └── version_info.txt
├── releases/                    # Final installers/executables
│   ├── windows/                 # Windows .exe
│   ├── macos/                   # macOS .app
│   └── linux/                   # Linux binary
├── assets/                      # Icons and branding
└── .gitignore
```
## Quick Start
### For End Users
Download the appropriate executable from the `releases/` folder for your platform and run it directly.

### For Developers
#### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
#### Running from Source
```bash
cd source
pip install -r requirements.txt
python gui_app.py
```
#### Building Executables
##### Windows
```cmd
cd source
BUILD_EXE.bat
```
Output: `releases/windows/SpectrumTek_Commissions_Converter.exe` 

##### macOS
```bash
cd source
chmod +x BUILD_APP.sh
./BUILD_APP.sh
```
Output: `releases/macos/SpectrumTek Commissions Converter.app` 

##### Linux
```bash
cd source
chmod +x BUILD_LINUX.sh
./BUILD_LINUX.sh
```
Output: `releases/linux/SpectrumTek_Commissions_Converter` 

## Workflow
1. **Clone the repository**git clone https://github.com/aaronwesthoff84/SpectrumTek-Commissions-Converter.git
cd SpectrumTek-Commissions-Converter
2. **Navigate to source directory**cd source
3. **Run the appropriate build script for your platform**
    - Windows: Double-click `BUILD_EXE.bat` 
    - macOS: Run `./BUILD_APP.sh` 
    - Linux: Run `./BUILD_LINUX.sh` 

4. **Find your built executable in the releases folder**
    - The build scripts automatically copy the final executable to `releases/<platform>/` 

5. **Commit and push if sharing the built installer**git add releases/
git commit -m "Add built executable for <platform>"
git push
## Command Line Usage
For CLI usage without the GUI:

```bash
cd source
python parse_commissions_xml.py "path/to/plan.xml" -o "output.xlsx"
```
## Documentation
- [﻿Developer Guide](docs/DEVELOPER_GUIDE.md)  - Comprehensive guide for developers: architecture overview, file reference, modification scenarios, and troubleshooting
- [﻿Build Guide](docs/BUILD_GUIDE.md)  - Detailed build instructions, customization, and troubleshooting
## License
Copyright © SpectrumTek. All rights reserved.


<!-- eraser-additional-content -->
## Diagrams
<!-- eraser-additional-files -->
<a href="/README-SpectrumTek Commissions Converter-1.eraserdiagram" data-element-id="gz6abiKeW5btE-kCsk8Ur"><img src="/.eraser/67zAsElvi1XJAFC4BPjK___4xqNLncNtMS0PvahqcWUTnAkbAh1___---diagram----591c7a659e57bb2ab27bf4fd9f67d27b-SpectrumTek-Commissions-Converter.png" alt="" data-element-id="gz6abiKeW5btE-kCsk8Ur" /></a>
<!-- end-eraser-additional-files -->
<!-- end-eraser-additional-content -->
<!--- Eraser file: https://app.eraser.io/workspace/67zAsElvi1XJAFC4BPjK --->
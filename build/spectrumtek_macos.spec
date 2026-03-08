# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for SpectrumTek Commissions Converter - macOS Build

This creates a macOS .app bundle that can be distributed to other macOS computers.

Usage:
    pyinstaller build/spectrumtek_macos.spec
"""

import sys
from pathlib import Path

# Get the project root directory
spec_dir = Path(SPECPATH).parent
project_dir = spec_dir

block_cipher = None

a = Analysis(
    [str(project_dir / 'gui_app.py')],
    pathex=[str(project_dir)],
    binaries=[],
    datas=[
        # Include the sap_commissions_xml package
        (str(project_dir / 'sap_commissions_xml'), 'sap_commissions_xml'),
    ],
    hiddenimports=[
        'sap_commissions_xml',
        'sap_commissions_xml.parser',
        'sap_commissions_xml.writer',
        'sap_commissions_xml.logger',
        'sap_commissions_xml.function_parser',
        'sap_commissions_xml.cli',
        'openpyxl',
        'openpyxl.workbook',
        'openpyxl.worksheet',
        'openpyxl.utils',
        'openpyxl.styles',
        'openpyxl.cell',
        'et_xmlfile',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'cv2',
        'pytest',
        'unittest',
        '_pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SpectrumTek_Commissions_Converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window (GUI app)
    disable_windowed_traceback=False,
    argv_emulation=True,  # Enable for macOS
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SpectrumTek_Commissions_Converter',
)

app = BUNDLE(
    coll,
    name='SpectrumTek Commissions Converter.app',
    icon=str(project_dir / 'assets' / 'icon.icns') if (project_dir / 'assets' / 'icon.icns').exists() else None,
    bundle_identifier='com.spectrumtek.commissions-converter',
    info_plist={
        'CFBundleName': 'SpectrumTek Commissions Converter',
        'CFBundleDisplayName': 'SpectrumTek Commissions Converter',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'CFBundleExecutable': 'SpectrumTek_Commissions_Converter',
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': 'STKC',
        'LSMinimumSystemVersion': '10.13.0',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,  # Support Dark Mode
    },
)

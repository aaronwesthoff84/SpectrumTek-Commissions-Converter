# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for SpectrumTek Commissions Converter - Portable (Single-File) Build

This creates a single .exe file that contains everything needed to run the application.
Pros: Easy to distribute, no installation required
Cons: Larger file size, slightly slower startup (extracts to temp folder)

Usage (from source/ directory):
    pyinstaller build_config/spectrumtek_portable.spec
"""

import sys
from pathlib import Path

# Get the source directory (spec is in source/build_config/)
spec_dir = Path(SPECPATH)
source_dir = spec_dir.parent  # Go up from build_config/ to source/
project_root = source_dir.parent  # Go up from source/ to project root

block_cipher = None

a = Analysis(
    [str(source_dir / 'gui_app.py')],
    pathex=[str(source_dir)],
    binaries=[],
    datas=[
        # Include the sap_commissions_xml package
        (str(source_dir / 'sap_commissions_xml'), 'sap_commissions_xml'),
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

# Check for icon and version info files
icon_path = project_root / 'assets' / 'icon.ico'
version_path = spec_dir / 'version_info.txt'

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SpectrumTek_Commissions_Converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (GUI app)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(icon_path) if icon_path.exists() else None,
    version=str(version_path) if version_path.exists() else None,
)

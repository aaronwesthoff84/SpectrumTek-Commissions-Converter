#!/bin/bash

# ============================================================
#   SpectrumTek Commissions Converter - macOS App Builder
#   Run this script to build your .app bundle!
# ============================================================

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}=                                                          =${NC}"
echo -e "${BLUE}=     SpectrumTek Commissions Converter - macOS Builder    =${NC}"
echo -e "${BLUE}=                                                          =${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""
echo "  This script will build a macOS .app bundle of the"
echo "  SpectrumTek Commissions XML-to-Excel Converter."
echo ""
echo "  The .app bundle can be distributed to any macOS computer"
echo "  running macOS 10.13 (High Sierra) or later."
echo ""
read -p "  Press Enter to start building, or Ctrl+C to cancel..."

# Change to script directory (source/)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
SOURCE_DIR="$PWD"
PROJECT_ROOT="$SOURCE_DIR/.."
RELEASES_DIR="$PROJECT_ROOT/releases/macos"

echo ""
echo -e "${YELLOW}[Step 1/5] Checking Python installation...${NC}"
echo "  ------------------------------------------"

# Check for Python 3
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    # Check if python is version 3
    if python --version 2>&1 | grep -q "Python 3"; then
        PYTHON_CMD="python"
        PIP_CMD="pip"
    else
        echo -e "${RED}ERROR: Python 3 is required but not found!${NC}"
        echo ""
        echo "  To install Python 3 on macOS:"
        echo "    1. Install Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        echo "    2. Run: brew install python3"
        echo "  Or download from: https://www.python.org/downloads/"
        exit 1
    fi
else
    echo -e "${RED}ERROR: Python is not installed!${NC}"
    echo ""
    echo "  To install Python 3 on macOS:"
    echo "    1. Install Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo "    2. Run: brew install python3"
    echo "  Or download from: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo -e "${GREEN}  SUCCESS: $PYTHON_VERSION is installed${NC}"
echo ""

echo -e "${YELLOW}[Step 2/5] Installing required packages...${NC}"
echo "  ------------------------------------------"
echo "  Installing PyInstaller and openpyxl..."

$PIP_CMD install pyinstaller openpyxl --quiet 2>/dev/null
if [ $? -ne 0 ]; then
    echo "  Trying with --user flag..."
    $PIP_CMD install pyinstaller openpyxl --user --quiet 2>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERROR: Failed to install required packages!${NC}"
        echo "  Try running: $PIP_CMD install pyinstaller openpyxl"
        exit 1
    fi
fi
echo -e "${GREEN}  SUCCESS: All required packages are installed${NC}"
echo ""

echo -e "${YELLOW}[Step 3/5] Cleaning up old builds...${NC}"
echo "  ------------------------------------"

rm -rf "$SOURCE_DIR/dist" 2>/dev/null
rm -rf "$SOURCE_DIR/build_temp" 2>/dev/null
rm -rf "$SOURCE_DIR/__pycache__" 2>/dev/null
rm -rf "$SOURCE_DIR/sap_commissions_xml/__pycache__" 2>/dev/null

echo -e "${GREEN}  SUCCESS: Cleaned up old files${NC}"
echo ""

echo -e "${YELLOW}[Step 4/5] Building the macOS application...${NC}"
echo "  -------------------------------------------"
echo "  This may take 1-3 minutes. Please be patient..."
echo ""

# Run PyInstaller with the macOS spec file
pyinstaller build_config/spectrumtek_macos.spec --clean --noconfirm --workpath=build_temp --distpath=dist 2>&1

if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: The build process failed!${NC}"
    echo ""
    echo "  Common solutions:"
    echo "    - Ensure Xcode Command Line Tools are installed: xcode-select --install"
    echo "    - Try running with sudo if permission errors occur"
    echo "    - Check that all project files are present"
    exit 1
fi

# Clean up temp build folder
rm -rf "$SOURCE_DIR/build_temp" 2>/dev/null

echo ""
echo -e "${YELLOW}[Step 5/5] Verifying the build and copying to releases...${NC}"
echo "  ---------------------------------------------------------"

APP_PATH="$SOURCE_DIR/dist/SpectrumTek Commissions Converter.app"

if [ -d "$APP_PATH" ]; then
    # Create releases directory if it doesn't exist
    mkdir -p "$RELEASES_DIR"
    
    # Copy to releases folder
    rm -rf "$RELEASES_DIR/SpectrumTek Commissions Converter.app" 2>/dev/null
    cp -R "$APP_PATH" "$RELEASES_DIR/"
    
    APP_SIZE=$(du -sh "$RELEASES_DIR/SpectrumTek Commissions Converter.app" | cut -f1)
    
    echo ""
    echo -e "${GREEN}============================================================${NC}"
    echo -e "${GREEN}=                                                          =${NC}"
    echo -e "${GREEN}=                   BUILD SUCCESSFUL!                      =${NC}"
    echo -e "${GREEN}=                                                          =${NC}"
    echo -e "${GREEN}============================================================${NC}"
    echo ""
    echo "  Your macOS app bundle has been created:"
    echo ""
    echo "    Location: $RELEASES_DIR/"
    echo "    Filename: SpectrumTek Commissions Converter.app"
    echo "    Size:     $APP_SIZE"
    echo ""
    echo "  You can now:"
    echo "    - Double-click the .app to run it"
    echo "    - Drag it to your Applications folder"
    echo "    - Share it with your team (create a .dmg for distribution)"
    echo ""
    echo -e "${GREEN}============================================================${NC}"
    echo ""
    
    # On macOS, offer to open the folder
    read -p "  Would you like to open the output folder? (y/n): " OPEN_FOLDER
    if [[ "$OPEN_FOLDER" == "y" || "$OPEN_FOLDER" == "Y" ]]; then
        open "$RELEASES_DIR"
    fi
else
    echo -e "${RED}ERROR: The .app bundle was not created.${NC}"
    echo "  Check the output above for error messages."
    exit 1
fi

echo ""
echo "  Build complete! Press Enter to exit..."
read

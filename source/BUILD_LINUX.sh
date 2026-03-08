#!/bin/bash

# ============================================================
#   SpectrumTek Commissions Converter - Linux Builder
#   Run this script to build your Linux executable!
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
echo -e "${BLUE}=     SpectrumTek Commissions Converter - Linux Builder    =${NC}"
echo -e "${BLUE}=                                                          =${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""
echo "  This script will build a Linux executable of the"
echo "  SpectrumTek Commissions XML-to-Excel Converter."
echo ""
echo "  The executable is a single portable file that runs on"
echo "  most Linux distributions with a GUI environment."
echo ""
read -p "  Press Enter to start building, or Ctrl+C to cancel..."

# Change to script directory (source/)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
SOURCE_DIR="$PWD"
PROJECT_ROOT="$SOURCE_DIR/.."
RELEASES_DIR="$PROJECT_ROOT/releases/linux"

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
        echo "  To install Python 3 on Ubuntu/Debian:"
        echo "    sudo apt update && sudo apt install python3 python3-pip python3-tk"
        echo ""
        echo "  On Fedora/RHEL:"
        echo "    sudo dnf install python3 python3-pip python3-tkinter"
        exit 1
    fi
else
    echo -e "${RED}ERROR: Python is not installed!${NC}"
    echo ""
    echo "  To install Python 3 on Ubuntu/Debian:"
    echo "    sudo apt update && sudo apt install python3 python3-pip python3-tk"
    echo ""
    echo "  On Fedora/RHEL:"
    echo "    sudo dnf install python3 python3-pip python3-tkinter"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo -e "${GREEN}  SUCCESS: $PYTHON_VERSION is installed${NC}"
echo ""

# Check for tkinter (required for GUI)
echo "  Checking for tkinter support..."
$PYTHON_CMD -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: tkinter is not installed!${NC}"
    echo ""
    echo "  To install tkinter on Ubuntu/Debian:"
    echo "    sudo apt install python3-tk"
    echo ""
    echo "  On Fedora/RHEL:"
    echo "    sudo dnf install python3-tkinter"
    exit 1
fi
echo -e "${GREEN}  SUCCESS: tkinter is available${NC}"
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

echo -e "${YELLOW}[Step 4/5] Building the Linux executable...${NC}"
echo "  ------------------------------------------"
echo "  This may take 1-3 minutes. Please be patient..."
echo ""

# Run PyInstaller with the Linux spec file
pyinstaller build_config/spectrumtek_linux.spec --clean --noconfirm --workpath=build_temp --distpath=dist 2>&1

if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: The build process failed!${NC}"
    echo ""
    echo "  Common solutions:"
    echo "    - Ensure you have build tools: sudo apt install build-essential"
    echo "    - Try running with different Python version"
    echo "    - Check that all project files are present"
    exit 1
fi

# Clean up temp build folder
rm -rf "$SOURCE_DIR/build_temp" 2>/dev/null

echo ""
echo -e "${YELLOW}[Step 5/5] Verifying the build and copying to releases...${NC}"
echo "  ---------------------------------------------------------"

EXE_PATH="$SOURCE_DIR/dist/SpectrumTek_Commissions_Converter"

if [ -f "$EXE_PATH" ]; then
    # Create releases directory if it doesn't exist
    mkdir -p "$RELEASES_DIR"
    
    # Copy to releases folder
    cp "$EXE_PATH" "$RELEASES_DIR/"
    chmod +x "$RELEASES_DIR/SpectrumTek_Commissions_Converter"
    
    EXE_SIZE=$(du -h "$RELEASES_DIR/SpectrumTek_Commissions_Converter" | cut -f1)
    
    echo ""
    echo -e "${GREEN}============================================================${NC}"
    echo -e "${GREEN}=                                                          =${NC}"
    echo -e "${GREEN}=                   BUILD SUCCESSFUL!                      =${NC}"
    echo -e "${GREEN}=                                                          =${NC}"
    echo -e "${GREEN}============================================================${NC}"
    echo ""
    echo "  Your Linux executable has been created:"
    echo ""
    echo "    Location: $RELEASES_DIR/"
    echo "    Filename: SpectrumTek_Commissions_Converter"
    echo "    Size:     $EXE_SIZE"
    echo ""
    echo "  You can now:"
    echo "    - Run it directly: ./releases/linux/SpectrumTek_Commissions_Converter"
    echo "    - Copy it to any Linux computer with a GUI"
    echo "    - Share it with your team"
    echo ""
    echo -e "${GREEN}============================================================${NC}"
    echo ""
    
    # Offer to open file manager
    read -p "  Would you like to open the output folder? (y/n): " OPEN_FOLDER
    if [[ "$OPEN_FOLDER" == "y" || "$OPEN_FOLDER" == "Y" ]]; then
        if command -v xdg-open &> /dev/null; then
            xdg-open "$RELEASES_DIR" 2>/dev/null &
        elif command -v nautilus &> /dev/null; then
            nautilus "$RELEASES_DIR" 2>/dev/null &
        fi
    fi
else
    echo -e "${RED}ERROR: The executable was not created.${NC}"
    echo "  Check the output above for error messages."
    exit 1
fi

echo ""
echo "  Build complete! Press Enter to exit..."
read

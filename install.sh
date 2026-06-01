#!/bin/bash

# Volk_4on_ok WoT Toolkit - Mac/Linux Installer
# For macOS and Linux distributions

echo ""
echo "============================================================"
echo "   VOLK_4ON_OK WOT TOOLKIT v2.0 - Mac/Linux Installer"
echo "============================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo "Please install Python 3.8+ from python.org"
    echo ""
    exit 1
fi

echo "[1/4] Checking Python version..."
python3 --version
echo ""

echo "[2/4] Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies!"
    exit 1
fi
echo ""

echo "[3/4] Creating shortcuts..."
cat > volk_toolkit << 'EOF'
#!/bin/bash
python3 "$(dirname "$0")/volk_wot_toolkit.py" "$@"
EOF
chmod +x volk_toolkit

cat > volk_mod << 'EOF'
#!/bin/bash
python3 "$(dirname "$0")/volk_4on_ok_mod.py" "$@"
EOF
chmod +x volk_mod

cat > volk_jokes << 'EOF'
#!/bin/bash
python3 "$(dirname "$0")/random_joke_generator.py" "$@"
EOF
chmod +x volk_jokes
echo ""

echo "[4/4] Testing installation..."
python3 volk_wot_toolkit.py > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "WARNING: Installation may have issues"
else
    echo ""
fi

echo "============================================================"
echo "   INSTALLATION COMPLETE!"
echo "============================================================"
echo ""
echo "Quick Start:"
echo "  ./volk_toolkit           - Run WoT Toolkit"
echo "  ./volk_mod               - Run WoT Mod"
echo "  ./volk_jokes             - Run Joke Generator"
echo ""
echo "Or use command line:"
echo "  python3 volk_wot_toolkit.py interactive"
echo "  python3 volk_4on_ok_mod.py"
echo "  python3 random_joke_generator.py interactive"
echo ""
echo "Documentation: README.md"
echo ""

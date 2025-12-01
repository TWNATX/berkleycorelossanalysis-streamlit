#!/bin/bash

echo "========================================"
echo "BerkleyCore Loss Analysis Platform"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Install with: brew install python (Mac) or apt install python3 (Linux)"
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

echo ""
echo "Starting BerkleyCore..."
echo "Your browser will open to http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py

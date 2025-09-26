#!/bin/bash

echo "Setting up Python environment for CLIP API..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from your package manager or https://python.org"
    exit 1
fi

# Create virtual environment
echo "Creating Python virtual environment..."
if [ -d "python-env" ]; then
    echo "Removing existing environment..."
    rm -rf python-env
fi

python3 -m venv python-env
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

# Activate environment and install dependencies
echo "Activating environment and installing dependencies..."
source python-env/bin/activate

# Upgrade pip first
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Python dependencies"
    exit 1
fi

echo ""
echo "✅ Python environment setup complete!"
echo ""
echo "To activate the environment manually:"
echo "  source python-env/bin/activate"
echo ""
echo "To test the setup:"
echo "  npm run python:test"
echo ""
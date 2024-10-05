#!/bin/bash

# Check if python3-pip is installed already, if not, install it
if ! command -v pip3 &> /dev/null
then
    echo "python3-pip is not installed. Installing..."
    sudo apt install python3-pip -y
else
    echo "python3-pip is already installed."
fi

# Install UV for dependency management
pip3 install uv

# Create a virtual environment with UV
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

echo "Environment setup completed successfully!"
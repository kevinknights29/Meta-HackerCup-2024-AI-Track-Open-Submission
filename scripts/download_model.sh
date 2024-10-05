#!/bin/bash

# Check if python3-pip is installed already, if not, install it
if ! command -v pip3 &> /dev/null
then
    echo "python3-pip is not installed. Installing..."
    sudo apt install python3-pip -y
else
    echo "python3-pip is already installed."
fi

# Install huggingface transfer
uv pip install huggingface_hub[hf_transfer]

# Enable huggingface transfer
HF_HUB_ENABLE_HF_TRANSFER=1 

# Add repo id as input
echo "Please enter the Hugging Face repository ID:"
read repo_id

# Capture token for authenticated model downloads
echo "Please enter your Hugging Face token (input will be hidden):"
read -s token

huggingface-cli download "$repo_id" --token "$token" 

echo "Downloaded model!"

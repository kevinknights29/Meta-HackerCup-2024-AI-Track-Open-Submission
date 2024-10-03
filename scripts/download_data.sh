#!/bin/bash

# Check if python3-pip is installed already, if not, install it
if ! command -v pip3 &> /dev/null
then
    echo "python3-pip is not installed. Installing..."
    sudo apt install python3-pip -y
else
    echo "python3-pip is already installed."
fi

# Suppress warning if running pip as root
PIP_ROOT_USER_ACTION=ignore pip3 install huggingface_hub[hf_transfer]

HF_HUB_ENABLE_HF_TRANSFER=1 

huggingface-cli download hackercupai/hackercup --repo-type dataset --local-dir ./dataset

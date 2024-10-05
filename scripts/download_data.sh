#!/bin/bash

# Function to display usage information
usage() {
    echo "Usage: $0 <local_directory>"
    echo "Please provide a directory path for downloading the dataset."
    exit 1
}

# Check if exactly one argument is provided
if [ $# -ne 1 ]; then
    usage
fi

# Assign the provided directory to LOCAL_DIR
LOCAL_DIR="$1"

# Check if uv is installed already
if ! command -v uv &> /dev/null
then
    echo "Please run: . ./scripts/setup_env to have all necessary dependencies"
    exit 1
else
    echo "uv is installed."
fi

# Install huggingface transfer
uv pip install huggingface_hub[hf_transfer]

# Enable huggingface transfer
HF_HUB_ENABLE_HF_TRANSFER=1 

# Download dataset
huggingface-cli download hackercupai/hackercup --repo-type dataset --local-dir "$LOCAL_DIR"

echo "Dataset downloaded to $LOCAL_DIR!"

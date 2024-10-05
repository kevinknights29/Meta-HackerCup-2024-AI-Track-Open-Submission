#!/bin/bash

# Function to display usage information
usage() {
    echo "Usage: $0 <repo_id> $1 <local_directory>"
    echo "Please provide a directory path for downloading the dataset."
    exit 1
}

# Check if exactly one argument is provided
if [ $# -ne 2 ]; then
    usage
fi

# Assign the provided repo_id to REPO_ID
REPO_ID="$1"

# Assign the provided directory to LOCAL_DIR
LOCAL_DIR="$2"

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

# Capture token for authenticated model downloads
echo "Please enter your Hugging Face token (input will be hidden):"
read -s token

huggingface-cli download "$REPO_ID" --token "$token" --local-dir "$LOCAL_DIR/$REPO_ID"

echo "Downloaded model to $LOCAL_DIR/$REPO_ID!"

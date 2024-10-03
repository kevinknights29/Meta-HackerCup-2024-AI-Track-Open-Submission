# Meta-HackerCup-2024-AI-Track-Open-Submission

Repo to host my Meta HackerCup 2024 AI Track Open Submission.

## Pre-work

1. Create a VM that complies with the Open AI Track rules.

    > Open model - Solutions must be built using 1 single NVIDIA A100 graphics card with 40GB VRAM, no more than 128GB RAM and no more than 1TB of storage and must not use the internet (after all artifacts are downloaded).

    - I'm using an A100 VM from [Datacrunch.io](https://datacrunch.io/products#A100), due to their low pricing. ![image](https://github.com/user-attachments/assets/d0b06ed0-ff53-4598-a995-3d853f9546da)

2. Create an SSH key to access your VM.

    ```bash
    ssh-keygen -t ed25519 -C "<input>"
    ```

3. Create an SSH key for your GitHub account. Please refer to [Generating a new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).

4. Configure your git user.name and user.email.

    ```bash
    git config --global user.name "name"
    git config --global user.email "name@example.com"
    ```

## Getting Started

1. Clone the repo.

    ```bash
    git clone git@github.com:kevinknights29/Meta-HackerCup-2024-AI-Track-Open-Submission.git
    ```

2. Download model from HuggingFace running `scripts/download_model.sh`.

    - You will be prompted to type the repo id, i.e. `meta-llama/Llama-2-7b-hf`

    - Then, you will be prompted for your HuggingFace token for authentication. Please refer to [Security Tokens](https://huggingface.co/docs/hub/en/security-tokens)

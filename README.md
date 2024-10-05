# Meta-HackerCup-2024-AI-Track-Open-Submission

Repo to host my Meta HackerCup 2024 AI Track Open Submission.

## Pre-work

1. Create a VM that complies with the Open AI Track rules.

    > Open model - Solutions must be built using 1 single NVIDIA A100 graphics card with 40GB VRAM, no more than 128GB RAM and no more than 1TB of storage and must not use the internet (after all artifacts are downloaded).

    - I'm using an A100 VM from [Datacrunch.io](https://datacrunch.io/products#A100), due to their low pricing. ![image](https://github.com/user-attachments/assets/d0b06ed0-ff53-4598-a995-3d853f9546da)

    - I'm using a 100 GB volume from [Datacrunch.io](https://datacrunch.io), to optimize the cost of the vm. If I increase the volume of the boot disk when deploying the VM, the storage costs exceed the VM's cost. ![image](https://github.com/user-attachments/assets/4dfb2fae-4ee9-42c6-9baf-adfde4b2d122)

        > NOTE: I have a guide for mounting a volume [here](./scripts/mount_volume.md).

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

2. Download model from HuggingFace running `. scripts/download_model.sh <repo_id> <local_dir>`.

    - Then, you will be prompted for your HuggingFace token for authentication. Please refer to [Security Tokens](https://huggingface.co/docs/hub/en/security-tokens)

3. Download datasets from previous Hackercups with `. scripts/downlaod_dataset.sh <local_dir>`.

### Generating your first programs

1. Run `. scripts/setup_env.sh`.

2. Update `config.yaml` with your model, dataset, programs, and results directories.

3. Run `python generate_programs.py`.

4. Run `python evaluate_programs.py`.

#### My first results with `meta-llama/Llama-2-7b-hf`

| Problem | Score |
| ------- | ----- |
| 2012/round3/divisor_function_optimization | 0/60 |
| 2012/finals/linsane_phone_numbers | 0/15 |
| 2012/finals/maximal_multiplicative_order | 0/60 |
| 2012/quals/auction | FAIL |
| 2012/quals/alphabet_soup | 2/60 |
| 2012/quals/billboards | 0/60 |
| 2012/round1/checkpoint | FAIL |
| 2011/round1a/wine_tasting | 0/50 |
| 2011/round1b/diminishing_circle | 0/60 |
| 2011/round1b/slot_machine_hacker | FAIL |
| 2011/round2/studious_student_ii | 0/60 |
| 2011/round2/bonus_assignments | 0/60 |
| 2011/quals/double_squares | FAIL |
| 2011/quals/peg_game | FAIL |
| 2011/quals/studious_student | 21/39 |
| 2011/round1c/n_factorful | 1/50 |
| 2013/finals/teleports | 0/31 |
| 2013/finals/archiver | FAIL |
| 2013/finals/colored_trees | 0/60 |
| 2013/round2/cake_cutting | 0/50 |
| 2013/round2/roboelection | 6/100 |
| 2013/quals/beautiful_strings | FAIL |
| 2013/quals/balanced_smileys | FAIL |
| 2013/round1/dead_pixels | 0/40 |
| 2015/round2/all_critical | 0/98 |
| 2015/quals/cooking_the_books | 0/100 |
| 2015/round1/homework | 0/100 |
| 2015/round1/winning_at_sports | FAIL |
| 2017/finals/patrols | 0/30 |
| 2017/round2/subtlesabotage | 0/15005 |
| 2017/quals/progresspie | FAIL |
| 2014/quals/tennison | 0/92 |
| 2014/round1/coins_game | 7/31 |
| 2014/round1/labelmaker | FAIL |
| 2016/round2/carnival_coins | 0/509 |

## Deleting a Model

If you would like to delete a model downloaded locally, run `huggingface-cli delete-cache`.

Sample Output:

```text
? Select revisions to delete: 1 revision(s) selected.
? 1 revisions selected counting for 27.0G. Confirm deletion ? Yes
Start deletion.
Done. Deleted 1 repo(s) and 0 revision(s) for a total of 27.0G
```

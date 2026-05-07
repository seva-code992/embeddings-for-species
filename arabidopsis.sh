#!/bin/bash
#SBATCH --job-name=Arabidopsis_embeddings
#SBATCH --output=output_arabidopsis.txt
#SBATCH --time=10:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --gres=gpu:tesla:1
#SBATCH --partition=gpu




source .venv/bin/activate
uv run arabidopsis_embeddings.py
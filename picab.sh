#!/bin/bash
#SBATCH --job-name=Picab_embeddings
#SBATCH --output=output_picab.txt
#SBATCH --time=10:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4      
#SBATCH --mem=16G          
#SBATCH --gres=gpu:tesla:1   
#SBATCH --partition=gpu




source .venv/bin/activate
uv run picab_embeddings.py
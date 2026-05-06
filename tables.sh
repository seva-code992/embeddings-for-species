#!/bin/bash
#SBATCH --job-name=Fileprep
#SBATCH --output=output_fileprep.txt
#SBATCH --time=10:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4      
#SBATCH --mem=16G          
#SBATCH --gres=gpu:tesla:1   
#SBATCH --partition=gpu




uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
uv run fileprep.py
duckdb database.db
duckdb database.db -f export_modified_tables.sql
#!/bin/sh
#SBATCH --job-name=pykt_preprocess
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=24GB
#SBATCH --chdir=/home/koutchc1/pykt-toolkit
#SBATCH --output=/home/koutchc1/pykt-toolkit/logs/preprocessing/slurm_seq2seq_%A.out

module load miniconda;
source activate emnlp2023;

export PYTHONPATH="$HOME/pykt-toolkit"
export HF_DATASETS_CACHE="/scratch/work/koutchc1/cache/huggingface/datasets/"

python3 examples/data_preprocess.py --dataset_name="falconcode_2_2"

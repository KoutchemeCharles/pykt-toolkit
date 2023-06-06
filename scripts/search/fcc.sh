#!/bin/sh
#SBATCH --job-name=pykt_sakt_training
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=1
#SBATCH --gpus-per-node=1
#SBATCH --mem=8GB
#SBATCH --chdir=/home/koutchc1/pykt-toolkit
#SBATCH --output=/home/koutchc1/pykt-toolkit/logs/search/slurm_seq2seq_%A.out

module load miniconda;
source activate pykt;

export PYTHONPATH="$HOME/pykt-toolkit"
export HF_DATASETS_CACHE="/scratch/work/koutchc1/cache/huggingface/datasets/"
export CUDA_VISIBLE_DEVICES=1 

WANDB_API_KEY=ec630356a5b2818a01b9dc79163b363f78086ff2 wandb agent letech/kt_toolkits/68sluxig
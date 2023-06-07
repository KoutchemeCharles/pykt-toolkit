#!/bin/sh
#SBATCH --job-name=pykt_sweeping
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=1
#SBATCH --gpus-per-node=1
#SBATCH --mem=8GB
#SBATCH --array=1-5
#SBATCH --chdir=/home/koutchc1/pykt-toolkit
#SBATCH --output=/home/koutchc1/pykt-toolkit/logs/search/slurm_seq2seq_%A_%a.out

module load miniconda;
source activate pykt;

export PYTHONPATH="$HOME/pykt-toolkit"
export HF_DATASETS_CACHE="/scratch/work/koutchc1/cache/huggingface/datasets/"
export CUDA_VISIBLE_DEVICES=1 

n=$SLURM_ARRAY_TASK_ID
iteration=`head -n ${n} start_sweep_0_5.sh | tail -1` # Get n-th line (1-indexed) of the file
echo ${iteration}
WANDB_API_KEY=ec630356a5b2818a01b9dc79163b363f78086ff2 ${iteration}
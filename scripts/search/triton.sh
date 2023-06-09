#!/bin/sh
#SBATCH --job-name=pykt_sweeping
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=1
#SBATCH --gpus-per-node=1
#SBATCH --mem=10GB
#SBATCH --array=1-5
#SBATCH --chdir=/home/koutchc1/pykt-toolkit
#SBATCH --output=/home/koutchc1/pykt-toolkit/logs/search/slurm_seq2seq_%A_%a.out

module load miniconda;
source activate pykt;

export PYTHONPATH="$HOME/pykt-toolkit"
export HF_DATASETS_CACHE="/scratch/work/koutchc1/cache/huggingface/datasets/"
export WANDB_API_KEY=ec630356a5b2818a01b9dc79163b363f78086ff2

n=$SLURM_ARRAY_TASK_ID
sweeping=`head -n ${n} start_sweeps.log | tail -1` # Get n-th line (1-indexed) of the file
echo ${sweeping}
${sweeping}
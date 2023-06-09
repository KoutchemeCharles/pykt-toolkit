#!/bin/sh
#SBATCH --job-name=pykt_testing
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=1
#SBATCH --gpus-per-node=1
#SBATCH --mem=8GB
#SBATCH --array=1-5
#SBATCH --chdir=/home/koutchc1/pykt-toolkit
#SBATCH --output=/home/koutchc1/pykt-toolkit/logs/testing/slurm_seq2seq_%A_%a.out

module load miniconda;
source activate pykt;

export PYTHONPATH="$HOME/pykt-toolkit"
export HF_DATASETS_CACHE="/scratch/work/koutchc1/cache/huggingface/datasets/"

n=$SLURM_ARRAY_TASK_ID
path=`head -n ${n} /home/koutchc1/pykt-toolkit/best_models.txt | tail -1`
python ./examples/wandb_predict.py --save_dir=${path}
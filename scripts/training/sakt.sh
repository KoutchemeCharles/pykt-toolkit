#!/bin/sh
#SBATCH --job-name=pykt_sakt_training
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=1
#SBATCH --gpus-per-node=1
#SBATCH --mem=8GB
#SBATCH --chdir=/home/koutchc1/pykt-toolkit
#SBATCH --output=/home/koutchc1/pykt-toolkit/logs/training/slurm_seq2seq_%A.out

module load miniconda;
source activate pykt;

export PYTHONPATH="$HOME/pykt-toolkit"
export HF_DATASETS_CACHE="/scratch/work/koutchc1/cache/huggingface/datasets/"
export CUDA_VISIBLE_DEVICES=1 

# Training the model on our dataset 
python ./examples/wandb_sakt_train.py --dataset_name=falconcode_2_2
# Evaluating the trained model on the test set 
#!/bin/sh

module load miniconda;
source activate pykt;

export PYTHONPATH="$HOME/pykt-toolkit"
export HF_DATASETS_CACHE="/scratch/work/koutchc1/cache/huggingface/datasets/"
export CUDA_VISIBLE_DEVICES=1 

python generate_wandb.py --dataset_names="falconcode_2_2" --model_names="dkt"
sh all_start.sh > log.all 2>&1
sh ./examples/run_all.sh log.all 0 5 falconcode_2_2 dkt 1,1,1,1,1
sh start_sweep_0_5.sh
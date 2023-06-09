#!/bin/sh

module load miniconda;
source activate pykt;

export PYTHONPATH="$HOME/pykt-toolkit"
export HF_DATASETS_CACHE="/scratch/work/koutchc1/cache/huggingface/datasets/"

python generate_wandb.py --dataset_names="falconcode_2_2,falconcode_2_3" --model_names="dkt,dkvmn,akt" --launch_file="all_start.sh"
sh all_start.sh > log.all 2>&1
python examples/all_start.py --directed_log="log.all"
sbatch "/home/koutchc1/pykt-toolkit/scripts/search/triton.sh"


# Run the code with the best hyperparameters 
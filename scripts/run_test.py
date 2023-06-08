""" Run the testing of the models pipeline. """


from argparse import ArgumentParser
from textwrap import dedent

from pykt.utils.files import json2data


def create_slurm_script(dataset_name, model_name, best_hyperparams):

    param_str = [f"--{k}={repr(v)}" for k, v in best_hyperparams]
    retrain_str = f"python wandb_{model_name}_train.py "
    retrain_str += f"--dataset_name={dataset_name} {param_str} "
    retrain_str += "--use_wandb=1 --add_uuid=0"

    template = f"""
    #!/bin/sh
    #SBATCH --job-name=pykt_testing
    #SBATCH --time=24:00:00
    #SBATCH --cpus-per-task=1
    #SBATCH --gpus-per-node=1
    #SBATCH --mem=8GB
    #SBATCH --chdir=/home/koutchc1/pykt-toolkit
    #SBATCH --output=/home/koutchc1/pykt-toolkit/logs/testing/slurm_seq2seq_%A.out

    module load miniconda;
    source activate pykt;

    export PYTHONPATH="$HOME/pykt-toolkit"
    export HF_DATASETS_CACHE="/scratch/work/koutchc1/cache/huggingface/datasets/"
    export CUDA_VISIBLE_DEVICES=1 

    # We train the model a final time using the found best hyperparameters
    {retrain_str}

    # We extract the last line which contains the model save dir
    iteration=`sed -n '/^MODEL_SAVE_DIR\|^B/p' test.log`


    python examples/wandb_predict.py --save_dir /scatch/work/koutchc1/
    
    """
    
    template = dedent(template.strip())



def parse_args():
    description = "Final evaluation of a model on a given dataset."
    parser = ArgumentParser(description=description)
    parser.add_argument("--dataset_names", type=str, default="falconcode_2_2")
    parser.add_argument("--model_names", type=str, default="dkt")
    parser.add_argument("--best_model_path", type=str, default="/home/koutchc1/pykt-toolkit/configs/best_model.json")

    return parser.parse_args()

def main():
    args = vars(parse_args())
    # Load the file with the best hyperparameters
    selected_datasets = args["dataset_names"].split(",")
    selected_models = args["model_names"].split(",")
    best_models = json2data(args["best_hyperparams_path"])

    for dataset, model_to_params in best_models.items():
        if (not selected_datasets) or dataset in selected_datasets:
            for model in selected_models:
                if (not selected_models) or model in selected_models:



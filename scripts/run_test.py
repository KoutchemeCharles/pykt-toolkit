""" Run the testing of the models pipeline. """


from argparse import ArgumentParser
from textwrap import dedent

from pykt.utils.files import json2data


def create_slurm_script(n_models, models_fp):

    template = dedent("""
    #!/bin/sh
    #SBATCH --job-name=pykt_testing
    #SBATCH --time=24:00:00
    #SBATCH --cpus-per-task=1
    #SBATCH --gpus-per-node=1
    #SBATCH --mem=8GB
    """)

    template += f"#SBATCH --array=1-{n_models}"
    template += dedent("""
    #SBATCH --chdir=/home/koutchc1/pykt-toolkit
    #SBATCH --output=/home/koutchc1/pykt-toolkit/logs/testing/slurm_seq2seq_%A_%a.out

    module load miniconda;
    source activate pykt;

    export PYTHONPATH="$HOME/pykt-toolkit"
    export HF_DATASETS_CACHE="/scratch/work/koutchc1/cache/huggingface/datasets/"

    n=$SLURM_ARRAY_TASK_ID
    """)
    
    template += 'path=`head -n ${n} ' + f"{models_fp} | tail -1`\n" # Get n-th line (1-indexed) of the file\n"
    template += "python ./examples/wandb_predict.py --save_dir=${path}"
    template = dedent(template.strip())

    print(template)
    return template

def parse_args():
    description = "Final evaluation of a model on a given dataset."
    parser = ArgumentParser(description=description)
    parser.add_argument("--best_model_path", type=str, default="/home/koutchc1/pykt-toolkit/best_models.txt")

    return parser.parse_args()

def main():
    # TODO: here need to analyze the resuls with the script that was on the jupyter notebook 
    args = vars(parse_args())
    with open(args["best_model_path"], 'r') as fp:
        n_lines = len(fp.readlines())
    
    bash_script = create_slurm_script(n_lines, args["best_model_path"])
    with open("/home/koutchc1/pykt-toolkit/scripts/testing/triton.sh", "w") as fin:
        fin.write(bash_script)
    
if __name__ == "__main__":
    main()

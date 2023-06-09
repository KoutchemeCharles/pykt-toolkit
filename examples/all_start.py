import os
import json 
from argparse import ArgumentParser
from textwrap import dedent
                         
def parse_args():
    description = "Runs all the sweep agents for all sweep configuration."
    parser = ArgumentParser(description=description)
    parser.add_argument("--directed_log", default="log.all")
    parser.add_argument("--output_log", default="start_sweeps.log")
    parser.add_argument("--project_name", default="emnlp2023")
    parser.add_argument("--dataset_names", type=str, default="falconcode_2_2")
    parser.add_argument("--model_names", type=str, default="dkt")

    return parser.parse_args()

def get_wandb_api():
    api_key = os.getenv("WANDB_API_KEY")
    if api_key == None:
        with open("/home/koutchc1/pykt-toolkit/configs/wandb.json") as fin:
            wandb_config = json.load(fin)
            api_key = wandb_config["api_key"]
    return api_key

def check_dataset(fname, dataset_names):
    if not dataset_names: return True
    for name in dataset_names:
        if fname.startswith(name):
            return True 
    return False 

def check_model(fname, model_names):
    if not model_names: return True
    for name in model_names:
        if fname.find("_" + name + "_") != -1:
            return True 
    return False 

def create_sweep_logs(input_log, output_log, dataset_names, model_names):
    sweeps = []
    with open(input_log, "r") as fin:
        i = 0
        lines = fin.readlines()
        while i < len(lines):
            if lines[i].strip().startswith("wandb: Creating sweep from: "):
                fname = lines[i].strip().split(": ")[-1].split("/")[-1]
            else:
                print("error!")
            if lines[i+3].strip().startswith("wandb: Run sweep agent with: "):
                sweepid = lines[i+3].strip().split(": ")[-1]
            else:
                print("error!")
            fname = fname.split(".")[0]
            # print(f"fname is {fname}")
            if check_dataset(fname, dataset_names) \
                and check_model(fname, model_names):
                sweeps.append(sweepid)
            i += 4

    with open(output_log, 'w') as f:
        for start_sweep in sweeps:
            f.write(f"{start_sweep}\n")

    return len(sweeps)


def create_bash_script(n_sweeps, wandb_api_key, log_path):
    template = dedent("""
    #!/bin/sh
    #SBATCH --job-name=pykt_sweeping
    #SBATCH --time=32:00:00
    #SBATCH --cpus-per-task=1
    #SBATCH --gpus-per-node=1
    #SBATCH --mem=10GB
    """)
    template += f"#SBATCH --array=1-{n_sweeps}"
    template += dedent("""
    #SBATCH --chdir=/home/koutchc1/pykt-toolkit
    #SBATCH --output=/home/koutchc1/pykt-toolkit/logs/search/slurm_seq2seq_%A_%a.out

    module load miniconda;
    source activate pykt;

    export PYTHONPATH="$HOME/pykt-toolkit"
    export HF_DATASETS_CACHE="/scratch/work/koutchc1/cache/huggingface/datasets/"
    """)
    template += f"export WANDB_API_KEY={wandb_api_key}\n\n"

    template += "n=$SLURM_ARRAY_TASK_ID\n"
    template += 'sweeping=`head -n ${n} ' + f"{log_path} | tail -1` # Get n-th line (1-indexed) of the file\n"
    template += "echo ${sweeping}\n"
    template += "${sweeping}"
    template = dedent(template.strip())

    print(template)

    with open("/home/koutchc1/pykt-toolkit/scripts/search/triton.sh", "w") as fin:
        fin.write(template)

def main():
    args = vars(parse_args())
    args["dataset_names"] = args["dataset_names"].split(",")
    args["model_names"] = args["model_names"].split(",")
    n_sweeps = create_sweep_logs(args["directed_log"], 
                                 args["output_log"],
                                 args["dataset_names"],
                                 args["model_names"])
    wandb_api_key = get_wandb_api()
    create_bash_script(n_sweeps, wandb_api_key, args["output_log"])

if __name__ == "__main__":
    main()
import os, sys
import json
from textwrap import dedent



WANDB_API_KEY = os.getenv("WANDB_API_KEY")
with open("/home/koutchc1/pykt-toolkit/configs/wandb.json") as fin:
    wandb_config = json.load(fin)
    if WANDB_API_KEY == None:
        WANDB_API_KEY = wandb_config["api_key"]
# print(WANDB_API_KEY)

logf = sys.argv[1]
outf = open(sys.argv[2], "w")
start = int(sys.argv[3])
end = int(sys.argv[4])

dataset_name = sys.argv[5]
model_name = sys.argv[6]
nums = sys.argv[7].split(",")
# print(f"{dataset_name}_{model_name}")
if len(sys.argv) == 8:
    project_name = "kt_toolkits"
else:
    project_name = sys.argv[8]

cmdpre = f"WANDB_API_KEY={WANDB_API_KEY} "
endcmdpre =f"WANDB_API_KEY={WANDB_API_KEY} "




idx = 0
with open(logf, "r") as fin:
    i = 0
    lines = fin.readlines()
    l = []
    num = 0
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
        if not fname.startswith(dataset_name) or fname.find("_" + model_name + "_") == -1:
            i += 4
            continue
        # print(f"dataset_name: {dataset_name}, model_name: {model_name}, fname: {fname}")
        if idx >= start and idx < end:
            cmd = sweepid
            outf.write(cmd + "\n")
            num += 1
        idx += 1
        i += 4


n_sweeps = end - start
template = """
#!/bin/sh
#SBATCH --job-name=pykt_sweeping
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=1
#SBATCH --gpus-per-node=1
#SBATCH --mem=8GB
"""
template += f"#SBATCH --array=1-{n_sweeps}"
template += """
#SBATCH --chdir=/home/koutchc1/pykt-toolkit
#SBATCH --output=/home/koutchc1/pykt-toolkit/logs/search/slurm_seq2seq_%A_%a.out

module load miniconda;
source activate pykt;

export PYTHONPATH="$HOME/pykt-toolkit"
export HF_DATASETS_CACHE="/scratch/work/koutchc1/cache/huggingface/datasets/"
export CUDA_VISIBLE_DEVICES=1 

n=$SLURM_ARRAY_TASK_ID
"""

template += 'iteration=`head -n ${n} ' + f"{sys.argv[2]} | tail -1` # Get n-th line (1-indexed) of the file\n"
template += "echo ${iteration}\n"
template += cmdpre + "${iteration}"
template = dedent(template.strip())

print(template)

with open("/home/koutchc1/pykt-toolkit/scripts/search/triton.sh", "w") as fin:
    fin.write(template)
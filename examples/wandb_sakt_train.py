import argparse
from wandb_train import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_name", type=str, default="assist2015")
    parser.add_argument("--model_name", type=str, default="sakt")
    parser.add_argument("--emb_type", type=str, default="qid")
    parser.add_argument("--save_dir", type=str, default="saved_model")
    # parser.add_argument("--learning_rate", type=float, default=1e-5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--fold", type=int, default=0)
    parser.add_argument("--dropout", type=float, default=0.2)
    
    parser.add_argument("--emb_size", type=int, default=256)
    parser.add_argument("--learning_rate", type=float, default=1e-3)
    parser.add_argument("--num_attn_heads", type=int, default=8)
    parser.add_argument("--num_en", type=int, default=1)
    parser.add_argument("--use_wandb", type=int, default=1)
    parser.add_argument("--add_uuid", type=int, default=1)
    parser.add_argument("--kt_config_path", default="/home/koutchc1/pykt-toolkit/configs/kt_config.json")
    parser.add_argument("--data_config_path", default="/home/koutchc1/pykt-toolkit/configs/data_config.json")
    
    
    args = parser.parse_args()

    params = vars(args)
    print(params)
    main(params)

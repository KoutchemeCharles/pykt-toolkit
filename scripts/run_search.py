""" Run the whole hyperparameter search procedure on the triton cluster. """

from argparse import ArgumentParser

def parse_args():
    description="Run the hyperparameter search procedure"
    parser = ArgumentParser(description=description)

    return parser.parse_args()

def main():
    args = vars(parse_args())



if __name__ == "__main__":
    main()

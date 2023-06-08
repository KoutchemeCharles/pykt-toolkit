import os, json
from pathlib import Path
from shutil import rmtree
from dotmap import DotMap

def json2data(filename):
    """ loads a json file into a list (od dictionaries) """
    with open(filename,'r') as json_file:
        data = json.load(json_file)
    return data
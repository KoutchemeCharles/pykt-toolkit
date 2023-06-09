import json

def json2data(filename):
    """ loads a json file into a list (od dictionaries) """
    with open(filename,'r') as json_file:
        data = json.load(json_file)
    return data

def save(file, text):
    """ Saves a text in a text file. """
    with open(file, 'w') as fp:
        fp.write(str(text))

def save_json(data, filename):
    """ Saves data as json. """
    with open(filename, 'w') as fp:
        json.dump(data, fp)

def read_config(filename):
    """ Read a dictionary in a configuration format and transforms it into DotMap."""
    return DotMap(json2data(filename))
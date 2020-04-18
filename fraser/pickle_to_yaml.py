'''
The purpose of this module is to take a pickle file
from the pickle directory and dump it as a yaml file
into the yamml directory.
'''

import config
import pickle
import os
from collections import namedtuple
import ruamel.yaml

Text_Chunk = namedtuple('Text_Chunk', 'text_chunk start end type')

PICKLE_EXTENSION = "p"
YAML_EXTENSION = "yaml"


def pickle_to_yaml(file_name):

    cf = config.ConfigFile()
    pickle_files_path = (cf.configfile[cf.computername]['pickle_files_path'])
    pickle_file_path = pickle_files_path + file_name + os.extsep + PICKLE_EXTENSION

    with open(pickle_file_path, 'rb') as pickle_file:
        file_to_process = pickle.load(pickle_file)

    yaml_files_path = (cf.configfile[cf.computername]['yaml_files_path'])
    yaml_file_path = yaml_files_path + file_name + os.extsep + YAML_EXTENSION

    # used 'unsafe' because i couldn't get the Text Chunk to work ...
    yaml = ruamel.yaml.YAML(typ='unsafe')

    with open(yaml_file_path, "w") as yaml_file:
        yaml.dump(file_to_process, yaml_file)
    return True


if __name__ == '__main__':

    import sys
    import argparse
    import ast

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the pickle_to_yaml function
    pickle_to_yaml_parser = subparsers.add_parser('pickle_to_yaml')
    pickle_to_yaml_parser.add_argument('file_name')
    pickle_to_yaml_parser.set_defaults(function = pickle_to_yaml)

    # parse the arguments
    arguments = parser.parse_args()
    arguments = vars(arguments) #convert from Namespace to dict

    #attempt to extract and then remove the function entry
    try:
        function_to_call = arguments['function'] 
    except KeyError:
        print ("You need a function name. Please type -h to get help")
        sys.exit()
    else:
        #remove the function entry as we are only passing arguments
        del arguments['function']
    
    if arguments:
        #remove any entries that have a value of 'None'
        #We are *assuming* that these are optional
        #We are doing this because we want the function definition to define
        #the defaults (NOT the function call)
        arguments = { k : v for k,v in arguments.items() if v is not None }

        #alter any string 'True' or 'False' to bools
        arguments = { k : ast.literal_eval(v) if v in ['True','False'] else v 
                                              for k,v in arguments.items() }       

    result = function_to_call(**arguments) #note **arguments works fine for empty dict {}
   
    print (result)

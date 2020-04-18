'''
The purpose of this module is to process the text file
containing the Māori sentences to be slotted.

Each sentence is assessed as to whether it is 
'Yes' - can be processed
'No' - can't be processed

At this stage, 15 March 2020 just going to process
simple sentences
'''

import config
import os
import yaml

TEXT_EXTENSION = "txt"
YAML_EXTENSION = "yaml"


def process_source_file(file_name):

    cf = config.ConfigFile()
    source_files_path = (cf.configfile[cf.computername]['source_files_path'])
    source_file_path = source_files_path + file_name + os.extsep + TEXT_EXTENSION

    # the dictionary to hold the results
    results = {}

    # read in each line from the source file
    with open(source_file_path, 'r') as f:
        source_file = f.readlines()

    for line_number, line in enumerate(source_file, start=1):
        results[f'{line_number:05}'] = line.split()

    print(results)
    post_gateway_files_path = (cf.configfile[cf.computername]['post_gateway_files_path'])
    post_gateway_file_path = post_gateway_files_path + file_name + \
                             os.extsep + YAML_EXTENSION
    with open(post_gateway_file_path, "w") as myfile:
        yaml.dump(results, myfile, allow_unicode=True)
    return True


if __name__ == '__main__':

    import sys
    import argparse
    import ast

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the get_all_entries function
    process_source_file_parser = subparsers.add_parser('process_source_file')
    process_source_file_parser.add_argument('file_name')
    process_source_file_parser.set_defaults(function = process_source_file)

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

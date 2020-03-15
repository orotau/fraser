'''
The purpose of this module is to pre process the text file
whose file_id is passed.

get_non_maori_words
looks for those words which are non maori thus allowing
the detection of any spelling mistakes

'''

import config
import os
import re
import maori_regex

def is_number(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True

def get_non_maori_words(file_id):

    TEXT_EXTENSION = "txt"
    # TAUIRA_FILE_ID = "hpk_tauira" # duplicated with the choices in the call

    cf = config.ConfigFile()
    text_files_path = (cf.configfile[cf.computername]['text_files_path'])
    text_file_path = text_files_path + file_id + os.extsep + TEXT_EXTENSION

    with open(text_file_path, 'r') as f:
        for line_number, line in enumerate(f):
            maori_words = re.findall(maori_regex.maori_word, line, re.VERBOSE | re.IGNORECASE)
            all_words = re.findall(r"\w+", line)
                                                    
            for word in all_words:
                if word not in maori_words and not is_number(word):                    
                        print(word)

if __name__ == '__main__':

    import sys
    import argparse
    import ast

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the get_non_maori_words function
    process_text_file_parser = subparsers.add_parser('get_non_maori_words')
    process_text_file_parser.add_argument('file_id', choices = ['hpk_tauira',
                                                                'hpk_definitions'])
    process_text_file_parser.set_defaults(function = get_non_maori_words)

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

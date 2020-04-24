import pprint
import config
import teina

def get_open_compounds_list(file_id = 'hpk_tauira'):

    # the file_id is used for the list of teina

    HPK_OPEN_COMPOUNDS_FILE_NAME = "hpk_open_compounds.txt"
    OTHER_OPEN_COMPOUNDS_FILE_NAME = "other_open_compounds.txt"

    cf = config.ConfigFile()
    text_files_path = (cf.configfile[cf.computername]['text_files_path'])

    open_compounds_list = []

    hpk_open_compounds_file_path = \
    text_files_path + HPK_OPEN_COMPOUNDS_FILE_NAME
 
    other_open_compounds_file_path = \
    text_files_path + OTHER_OPEN_COMPOUNDS_FILE_NAME 

    with open(hpk_open_compounds_file_path, 'r') as f:
        for line in f:
            open_compounds_list.append(line.replace('\n', ''))

    with open(other_open_compounds_file_path, 'r') as f:
        for line in f: 
            open_compounds_list.append(line.replace('\n', ''))  

    # add any teina that are themselves open compounds
    # and have a big brother in the list of open compounds
    for big_brother, little_brothers in teina.teina[file_id]:
        if big_brother in open_compounds_list:
            for little_brother in little_brothers:
                if ' ' in little_brother:                    
                    open_compounds_list.append(little_brother)
        else:
            # big brother not in the list of open compounds
            if ' ' in big_brother:
                print("Must add " + big_brother + " to open compounds")
                return False
            else:
                # not an open compound but it could have open compound teina
                for little_brother in little_brothers:
                    if ' ' in little_brother:                    
                        open_compounds_list.append(little_brother)                 

    # sort the list by length (longest at start)
    # to avoid say finding 'the banana' and never finding
    # 'longer version of the banana'

    open_compounds_list.sort(key=len, reverse=True)
    print ("hi")
    pprint.pprint(open_compounds_list)
    return open_compounds_list

get_open_compounds_list()

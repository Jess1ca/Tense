__author__ = 'user'
import os
import tempfile
import shutil
import sys
import getopt

from generate_tree_files import *
from tense_rulebased import mark_tense
from tense_learning import tense_learning_svm


DATA_FOLDER_NAME =  tempfile.mkdtemp()

def create_data_folders(fn):
    os.makedirs(os.path.join(DATA_FOLDER_NAME,UNMARKED_ARTICLES))
    os.makedirs(os.path.join(DATA_FOLDER_NAME,DEP_TREES))
    os.makedirs(os.path.join(DATA_FOLDER_NAME,TMP))

    f = open(fn,"r")
    file_id = 0
    for line in f:
        open(os.path.join(DATA_FOLDER_NAME,UNMARKED_ARTICLES,str(file_id)+".tml.0"),"w").write(line)
        file_id += 1
    f.close()


def print_results(tense_result):
    for res in tense_result:
        print "\t".join([res["Article"].split(".")[0],res["Word"],str(res["Token"]),res["Tense"]])

def usage():
    return "Usage: tense.py {rb|ml} <input_file>"

def parse_command(argv):
    method = None
    file = None
    try:
        opts, args = getopt.getopt(argv,"hm:f:",["method=","file="])
    except getopt.GetoptError:
        print usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print usage()
            sys.exit()
        elif opt in ("-m", "--method"):
            method = arg
            if method !=RB and method!=ML:
                print usage()
                sys.exit(2)
        elif opt in ("-f", "--file"):
            file = arg
    if not method or not  file:
        print usage()
        sys.exit(2)
    return method,file

method,input_file = parse_command(sys.argv[1:])


create_data_folders(input_file)
create_dep_trees(DATA_FOLDER_NAME)

if method == ML:
    from tempeval.definitions import *
    tense_result = tense_learning_svm.tense(TEMPEVAL_TRAINING,DATA_FOLDER_NAME)
    print_results(tense_result)
elif method == RB:
    tense_result_dict, tense_result_list = mark_tense.tense(DATA_FOLDER_NAME)
    print_results(tense_result_list)
shutil.rmtree(DATA_FOLDER_NAME)






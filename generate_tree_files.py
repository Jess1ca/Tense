__author__ = 'user'

import os
import os.path

from utils.definitions import *


dir_path = os.path.dirname(os.path.abspath(__file__))

def create_dep_trees(prefix):
    for root, _, files in os.walk(os.path.join(prefix , UNMARKED_ARTICLES)):
        for f in files:
            fullpath = os.path.join(root, f)
            tmp_fn = os.path.join(prefix , TMP , f +".tmp")
            parse_command =  "java -cp " + dir_path +"\"\\stanford_parser\\*\" edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat \"penn\" edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz "+ fullpath + " > " + tmp_fn
            os.popen(parse_command)
            #print parse_command
    for root, _, files in os.walk(os.path.join(prefix , UNMARKED_ARTICLES)):
        for f in files:
            tmp_fn = os.path.join(prefix , TMP , f +".tmp")
            dep_fn = os.path.join(prefix , DEP_TREES , f +".dep")
            convert_command = "java -cp " + dir_path +"/stanford_parser/stanford-parser.jar edu.stanford.nlp.trees.EnglishGrammaticalStructure -treeFile "+ tmp_fn + " -conllx -basic -makeCopulaHead -keepPunct > " + dep_fn
            os.popen(convert_command)


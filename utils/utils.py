__author__ = 'jessica'

from collections import defaultdict
import os
from definitions import *
import dependency_tree

from dependency_tree import tree_readers

# load dependency trees from file inp
def load_depTrees_from_file(inp):
    f =open(inp,'r')
    ret = dependency_tree.tree_readers.create_dep_trees_from_stream(f)
    f.close()
    return ret

def extract_sent_details(f):
    f_split = f.split(".tml")
    article = f_split[0] + ".tml"
    sent_i, sent_j = f.find("tml."), f.find(".dep")
    sent = int(f[sent_i+4:sent_j])
    return article,sent


def load_trees(prefix):
    trees = defaultdict(defaultdict)
    for root, _, files in os.walk(os.path.join(prefix , DEP_TREES)):
        for f in files:
            article,sent = extract_sent_details(f)
            trees[article][sent] = load_depTrees_from_file(os.path.join(prefix ,DEP_TREES, f) )
    return trees

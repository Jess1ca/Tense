__author__ = 'user'

from tense_rulebased.tense_rules import *

from utils.utils import *


def tense(dir_prefix):
    trees = load_trees(dir_prefix)
    tense_dict = defaultdict(dict)
    tense_list = []
    n_tokens = defaultdict(dict)
    pos = defaultdict(dict)
    inconsistent_trees = []
    for article in trees.keys():
        tense_dict[article] = defaultdict(list)
        n_tokens[article] = defaultdict(int)
        pos[article] = defaultdict(dict)
        for sent in trees[article].keys():
            if len(trees[article][sent]) != 1:
                inconsistent_trees.append( (article,sent) )
                continue
            tree = trees[article][sent][0]
            pos[article][sent] = {}
            all_nodes = tree.search(lambda x: x)
            for node in all_nodes:
                pos[article][sent][node.id -1] = node.pos
            for verb_tree in tree.collect_verbal_predicates():
                tense = get_tense(verb_tree)[0]
                aspect = True
                tense_dict[article][sent].append((verb_tree.word,verb_tree.id-1,tense,aspect))
                tense_list.append({"Word":verb_tree.word,"Token":verb_tree.id-1,"Tense":tense,"Article":article,"Sentence ID":sent })
            n_tokens[article][sent] = tree.n_tokens
    return tense_dict,tense_list#,n_tokens,pos,inconsistent_trees


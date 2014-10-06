__author__ = 'user'

from collections import defaultdict
import os

from sklearn import svm

from dependency_tree import tree_readers
import dependency_tree
from tense_learning import features
from utils.definitions import *


from utils.utils import *

def extract_event_details(line):
    line_split = line.split("\t")
    if len(line_split) <= 2:
        return None
    tense = line_split[2]
    word = line_split[0]
    token = int(line_split[1])
    aspect = ""
    if len(line_split) == 4:
        aspect = line_split[3]
    return word,token,tense,aspect

def load_gold_standard(prefix):
    tense_gs = defaultdict(dict)
    for root, _, files in os.walk(os.path.join(prefix , TENSE_FORMAT) ):
        for f in files:
            fullpath = os.path.join(root, f)
            sent_counter = 0
            tense_gs[f] = defaultdict(list)
            with open (fullpath, "r") as myfile:
                for line in myfile:
                    line = line.strip()
                    if line != "":
                        res = extract_event_details(line)
                        if res:
                            word,token,tense,aspect = res
                            if tense_gs[f].has_key(sent_counter) == False:
                                tense_gs[f][sent_counter] = defaultdict(str)
                            tense_gs[f][sent_counter][token] = tense
                    else:
                        sent_counter += 1
    return tense_gs



def create_vectors_from_data(prefix,training_data=True):
    if training_data:
        tense_gs = load_gold_standard(prefix)
    trees = load_trees(prefix)
    x = []
    y = []
    sentences = []
    unconsisntent_trees = 0
    for article in trees.keys():
        for sent in trees[article].keys():
            if len(trees[article][sent]) != 1:
                unconsisntent_trees += 1
                continue
            tree = trees[article][sent][0]
            for verb_tree in tree.collect_verbal_predicates():
                vector = features.get_vector(verb_tree)
                if training_data:
                    if tense_gs[article].has_key(sent)==False:
                        continue
                    tense = tense_gs[article][sent][verb_tree.id-1]
                    if tense == "":
                        continue
                    y.append(tense)
                x.append(vector)
                sentences.append({"Article":article,"Sentence ID":sent,"Sentence:":tree.get_original_sentence(True),"Word":verb_tree.word,"Token":verb_tree.id-1})
    return x,y,sentences

def test(clf,x,y,sentences):
    correct = 0
    for i,sent in zip(range(0,len(x)),sentences):
        res = clf.predict(x[i])[0]
        if res == y[i]:
            correct+=1
        else:
            None#print sent, res , y[i]
    return float(correct)/len(y)


def train(x,y):
    clf = svm.LinearSVC()
    clf.fit(x,y)
    return clf

def tense(learning_corpus_dir,dir_prefix):
    x,y,sentences = create_vectors_from_data(learning_corpus_dir)
    clf = train(x,y)
    x,y,sentences = create_vectors_from_data(dir_prefix,False)

    for i,sent in zip(range(0,len(x)),sentences):
        sentences[i]["Tense"] = clf.predict(x[i])[0]
    return sentences

__author__ = 'jessica'

import os
from tense_rulebased import mark_tense, evaluation
from definitions import *

dir_path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(os.path.dirname(dir_path) , TEMPEVAL_TRAINING)

# rulebased
my_tense_dict, my_tense_list = mark_tense.tense(path)

accuracy,recall = evaluation.evaluate(path, my_tense_dict)

print "Rulebased"
print "Accuracy: ", accuracy
print "Recall: ", recall


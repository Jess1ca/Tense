__author__ = 'jessica'

from tense_learning import evaluation
import os
from definitions import *

dir_path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(os.path.dirname(dir_path) , TEMPEVAL_TRAINING)

#SVM
print "Learning with SVM"
print "Accuracy: ", evaluation.evaluate(path)

__author__ = 'jessica'
from tense_learning.tense_learning_svm import *

def evaluate(prefix):
    n_train_examples = 3000
    x,y,sentences = create_vectors_from_data(prefix)
    clf = train(x[:n_train_examples],y[:n_train_examples])
    return test(clf,x[n_train_examples:],y[n_train_examples:],sentences)

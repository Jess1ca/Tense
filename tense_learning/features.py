import functools


from dependency_tree.definitions import *

PAST = 0
PRESENT = 1
FUTURE = 2

classes = {"past":PAST,"present":PRESENT,"future":FUTURE}

def get_class_id(tense):
    return classes[tense.lower()]

def feat_passive_with_child_pos():
    def feat_passive_with_child_pos(pos, predicate):
        passive_nodes = filter(lambda x:x.get_parent_relation() in passive_dependencies, predicate.children)
        if passive_nodes and predicate.pos == VBN:
            child = passive_nodes[0]
            if child.pos == pos :
                return 1
        return 0
    return [ functools.partial(feat_passive_with_child_pos,pos) for pos in VERB_POS ]

def feat_passive_with_child_word():
    def feat_passive_with_child_word(word, predicate):
        passive_nodes = filter(lambda x:x.get_parent_relation() in passive_dependencies, predicate.children)
        if passive_nodes and predicate.pos == VBN:
            child = passive_nodes[0]
            if child.word == word :
                return 1
        return 0
    return [ functools.partial(feat_passive_with_child_word,word) for word in [BE,"being"] ]

def feat_predicate_pos():
    def feat_predicate_pos(pos, predicate):
        if predicate.pos == pos :
            return 1
        return 0
    return [ functools.partial(feat_predicate_pos,pos) for pos in VERB_POS ]


def feat_predicate_aux_relation_pos():
    def feat_predicate_aux_relation_pos(pos_func, predicate):
        flag,span = predicate._get_span_of_filtered_children(pos_func)
        if flag :
            return 1
        return 0
    return [ functools.partial(feat_predicate_aux_relation_pos,pos_func) for pos_func in [VBN_been_child_func,VB_be_child_func,VB_have_child_func,TO_child_func,FUTURE_MD_child_func, VBD_child_func, VBN_child_func, VBZ_child_func, VBP_child_func] ]

def feat_passive_with_parent_word():
    def feat_passive_with_parent_word (word,predicate):
        if (predicate.parent.word.lower() == word) :
            return 1
        return 0
    return [ functools.partial(feat_passive_with_parent_word,word) for word in ["going", "about"] ]


def feat_passive_with_parent_pos():
    def feat_passive_with_parent_pos(pos,predicate):
        if (predicate.parent.pos == pos) :
            return 1
        return 0
    return [ functools.partial(feat_passive_with_parent_pos,pos) for pos in VERB_POS ]

def parent_relation (predicate):
    if predicate.get_parent_relation() in clausal_complement :
        return 1
    return 0


def parent_has_future_child (predicate):
    flag_FUTURE_MD,span_FUTURE_MD = predicate.parent._get_span_of_filtered_children(FUTURE_MD_child_func)
    if flag_FUTURE_MD :
        return 1
    return 0

features = feat_passive_with_child_pos() + feat_passive_with_child_word() + feat_predicate_pos() + feat_predicate_aux_relation_pos() + feat_passive_with_parent_word() + feat_passive_with_parent_pos() + [parent_relation,parent_has_future_child]


def get_vector(predicate):

    vector = []

    for f in range(0,len(features)):
        vector.append(features[f](predicate))

    return vector

__author__ = 'jessica'


aux_dependencies = ["aux" ]
aux_cop_dependencies = aux_dependencies + ["cop"]
passive_dependencies = ["auxpass"]# "csubjpass", "nsubjpass" also indicate passive, but must come with auxpass in the general case. For other cases see json_files/not_auxpass.json
negation_dependencies = ["neg"]
time_dependencies = ["tmod"]
subject_dependencies = ["subj","nsubj","nsubjpass","csubj","csubjpass"]
object_dependencies = ["obj","dobj","iobj","pobj"]
arguments_dependencies = ["arg","agent","comp","acomp","ccomp","xcomp"] + object_dependencies + subject_dependencies
clausal_complement = ["xcomp"]
adverb_dependencies = ["advmod"]
prepositions_dependencies = ["prep"]
prt_dependency = "prt"
mod_labels = ["amod", "vmod"] + adverb_dependencies


# POS tags
VB = "VB"       #Verb, base form
VBD = "VBD"     #Verb, past tense
VBG = "VBG"     #Verb, gerund or present participle
VBN = "VBN"     #Verb, past participle
VBP = "VBP"     #Verb, non-3rd person singular present
VBZ = "VBZ" 	#Verb, 3rd person singular present
VERB_POS = [VB,VBD,VBG,VBN,VBP,VBZ] # all types of verb pos
TO = "TO"
IN = "IN"
MD = "MD"
DOT = "."
COMMA = ","
#pos which will not be needed to cover
ignore_pos = [DOT,COMMA]


def aux_children_with_pos(pos_tag):
    return (lambda node: node.get_pos() == pos_tag and node.get_parent_relation() in aux_dependencies)



WILL = "will"
WONT = "wo"
WOULD = "would"
ll = "'ll"
HAVE = "have"
BE = "be"
BEEN = "been"
D = "'d"

FUTURE_MODALS = [WILL, WONT, WOULD, ll, D, "may", "might"] # "wo" is the Modal part of "won't"


# comparators for DepTree._get_span_of_filtered_children() method
VB_child_func = aux_children_with_pos(VB)
VBD_child_func = aux_children_with_pos(VBD)
VBN_child_func = aux_children_with_pos(VBN)
VBP_child_func = aux_children_with_pos(VBP)
VBZ_child_func = aux_children_with_pos(VBZ)
TO_child_func = aux_children_with_pos(TO)
VBD_or_VBN_child_func = lambda node: (node.get_pos() == VBD or node.get_pos() == VBN) and node.get_parent_relation() in aux_dependencies
VBP_or_VBZ_child_func = lambda node: (node.get_pos() == VBP or node.get_pos() == VBZ) and node.get_parent_relation() in aux_dependencies
FUTURE_MD_child_func = lambda node: node.get_pos() == MD and node.get_parent_relation() in aux_dependencies and node.get_word().lower() in FUTURE_MODALS
VB_have_child_func = lambda node: node.get_pos() == VB and node.get_parent_relation() in aux_dependencies and node.get_word().lower() == HAVE
VB_be_child_func = lambda node: node.get_pos() == VB and node.get_parent_relation() in aux_dependencies and node.get_word().lower() == BE
VBN_been_child_func = lambda node: node.get_pos() == VBN and node.get_parent_relation() in aux_dependencies and node.get_word().lower() == BEEN





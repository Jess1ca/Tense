__author__ = 'user'

from collections import defaultdict
import os

from utils.definitions import *


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
    gs_n_tokens = defaultdict(dict)
    for root, _, files in os.walk(os.path.join(prefix , TENSE_FORMAT) ):
        for f in files:
            fullpath = os.path.join(root, f)
            sent_counter = 0
            tense_gs[f] = defaultdict(list)
            gs_n_tokens[f] = defaultdict(int)
            with open (fullpath, "r") as myfile:
                for line in myfile:
                    line = line.strip()
                    if line != "":
                        gs_n_tokens[f][sent_counter] += 1
                        res = extract_event_details(line)
                        if res:
                            word,token,tense,aspect = res
                            tense_gs[f][sent_counter].append((word, token, tense,aspect))
                    else:
                        sent_counter += 1

    return tense_gs, gs_n_tokens

def get_correct_values(my_tense,gs_tense):
    correct_values_list = []
    for article in gs_tense.keys():
        if my_tense.has_key(article):
            for sent_id in gs_tense[article].keys():
                if my_tense[article].has_key(sent_id):
                    correct_values_list += list(set([(article,sent_id) + x[0:3] for x in my_tense[article][sent_id]]).intersection( set([(article,sent_id) + x[0:3] for x in gs_tense[article][sent_id]]) ))
    return correct_values_list

# def load_all_article_sentences(gs_tense,prefix,article):
#     sentences={}
#     for i in gs_tense[article].keys():
#         sentences[i] = (open(prefix + "\\" + UNMARKED_ARTICLES + "\\" +article + "."+str(i), "r").read().strip())
#     return sentences


# def get_incorrect_and_unknown_values(gs_tense, my_tense, article, sent ):
#     unknown = []
#     incorrect = []
#     correct_tense = defaultdict(list)
#     for tuple_gs in gs_tense[article][sent]:
#         word_gs, token_gs, tense_gs, aspect_gs = tuple_gs
#         found = False
#         for tuple_my in my_tense[article][sent]:
#             if found==True:
#                 break
#             word_my, token_my, tense_my , aspect_my = tuple_my
#             if word_gs==word_my and token_gs==token_my:
#                 found = True
#                 if tense_gs!=tense_my :
#                     if tense_my!="unknown":
#                         incorrect.append((sent,word_gs,tense_gs,aspect_gs,tense_my))
#                     else:
#                         unknown.append((sent,word_gs,tense_gs,aspect_gs,"unknown",pos[article][sent][token_gs]))
#                 else:
#                     if aspect_gs == "":
#                         correct_tense["no_aspect"].append((sent,word_gs,tense_gs,aspect_my))
#                     elif aspect_my == aspect_gs:
#                         correct_tense["correct_aspect"].append((sent,word_gs,tense_gs,aspect_gs))
#                     elif aspect_my == "":
#                         correct_tense["aspect_not_retrieved"].append((sent,word_gs,tense_gs,aspect_gs))
#                     elif aspect_my != aspect_gs:
#                         correct_tense["wrong_aspect"].append((sent,word_gs,tense_gs,aspect_gs,aspect_my))
#         if found == False:
#             if pos[article][sent].has_key(token_gs) == False:
#                 print(article,sent, token_gs)
#             else:
#                 unknown.append((sent,word_gs,tense_gs,aspect_gs,"",pos[article][sent][token_gs]))
#
#     return  incorrect, unknown, correct_tense


# def write_wrong_value_to_file(prefix,gs_tense,my_tense):
#     wrong_values_f = open("wrong_values","w")
#     unknown_values_f = open("unknown_values","w")
#
#     for article in gs_tense.keys():
#         sentences = load_all_article_sentences(gs_tense,prefix,article)
#         if my_tense.has_key(article):
#             for sent in gs_tense[article].keys():
#                 if my_tense[article].has_key(sent):
#                     incorrect, unknown , correct_tense = get_incorrect_and_unknown_values(gs_tense, my_tense, article, sent)
#                     for sent,word,tense_gs,aspect_gs,tense_my in incorrect:
#                         wrong_values_f.write(article + "\t" + str(sent) + "\t" + sentences[sent] + "\t" + word + "\t" + tense_gs + "\t" + aspect_gs + "\t" + tense_my +"\n" )
#                     for sent,word,tense_gs,aspect_gs,tense_my,pos in unknown:
#                         unknown_values_f.write(article + "\t" + str(sent) + "\t" + sentences[sent] + "\t" + word + "\t" + tense_gs + "\t" + aspect_gs + "\t" + tense_my +"\t" + pos+"\n" )
#                 else:
#                     for word,token,tense,aspect in gs_tense[article][sent]:
#                         unknown_values_f.write(article + "\t" + str(sent) + "\t" + sentences[sent] + "\t" + word + "\t" + tense  + "\t" + aspect + "\n" )
#         else:
#             for sent in gs_tense[article].keys():
#                 for word,token,tense,aspect in gs_tense[article][sent]:
#                     unknown_values_f.write(article + "\t" + str(sent) + "\t" + sentences[sent] + "\t" + word + "\t" + tense  + "\t" + aspect + "\n" )


def get_retrieved(gs_tense, my_tense):
    retrieved=0
    for article in gs_tense.keys():
        if my_tense.has_key(article):
            for sent in gs_tense[article].keys():
                if my_tense[article].has_key(sent):
                    for tuple1 in gs_tense[article][sent]:
                        found = False
                        for tuple2 in my_tense[article][sent]:
                            if found==True:
                                break
                            if tuple1[0]==tuple2[0] and tuple1[1]==tuple2[1] and tuple2[2] != "unknown":
                                retrieved += 1
                                found = True
    return  retrieved


# def get_correct_values_aspect(tense_correct_values,gs_tense, my_tense):
#     n_correct = 0
#     n_retrieved = 0
#     for article,sent,word,token,tense in tense_correct_values:
#         for i in range(0,len(gs_tense[article][sent])):
#             gs_token = gs_tense[article][sent][i][1]
#             gs_aspect = gs_tense[article][sent][i][3]
#             if gs_token == token:
#                 break
#
#         if gs_aspect != "":
#             for i in range(0,len(my_tense[article][sent])):
#                 my_token = my_tense[article][sent][i][1]
#                 my_aspect = my_tense[article][sent][i][3]
#                 if my_token == token:
#                     break
#
#             if my_aspect != "":
#                 n_retrieved += 1
#                 if my_aspect == gs_aspect :
#                     n_correct += 1
#
#     return n_correct, n_retrieved


def evaluate(prefix,my_tense):

    gs_tense,gs_n_tokens = load_gold_standard(prefix)

    relevant =  sum([len(gs_tense[article][sent]) for article in gs_tense.keys() for sent in gs_tense[article] ])
    retrieved = get_retrieved(gs_tense, my_tense)
    correct_values_list = get_correct_values(my_tense,gs_tense)
    correct_values = len(correct_values_list)

    accuracy = float(correct_values)/retrieved
    recall = float(correct_values)/relevant

    return accuracy,recall

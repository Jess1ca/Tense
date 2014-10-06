__author__ = 'jessica'
import re
from xml.dom import minidom
from nltk import word_tokenize
from collections import defaultdict

import os, os.path
from definitions import *
from utils.definitions import *

def get_sentences_nodes(fullpath):
    with open (fullpath, "r") as myfile:
        data=myfile.read().replace('\n', ' ')
        xml = minidom.parseString(data)
        sentences =  xml.childNodes[0].getElementsByTagName("s")
    return sentences

def write_clean_sentence_to_file(file,xml_sent):
    for child in xml_sent.childNodes:
        if child.nodeType == child.TEXT_NODE:
            file.write(child.nodeValue)
        else:
            file.write(child.childNodes[0].nodeValue)
    file.write("\n")


def generate_clean_articles(prefix):
    for root, _, files in os.walk(os.path.join(prefix ,DATA)):
        for f in files:
            fullpath = os.path.join(root, f)
            sentences = get_sentences_nodes(fullpath)
            for sent_id in range(0,len(sentences)):
                # extract only text from sentence and write it to a file
                org_sent_f = open(os.path.join(prefix , UNMARKED_ARTICLES , f + "." + str(sent_id)), "w")
                write_clean_sentence_to_file(org_sent_f,sentences[sent_id])

def tokenize(fn):
    words_tok = []
    dir_path = os.path.dirname(os.path.abspath(__file__))
    tok_command =  "java -cp " + dir_path + "/stanford_parser/stanford-parser.jar edu.stanford.nlp.process.PTBTokenizer -options normalizeParentheses=false,asciiQuotes=true,normalizeAmpersandEntity=true,normalizeSpace=false " +fn
    stream = os.popen(tok_command)
    print tok_command
    for line in stream:
        word = line.strip()
        words_tok.append(word)
    return words_tok


def generate_tense_format(prefix):

    def parse_tense_data(node,out_str,value):
        if node.getAttribute("tense") == "PASTPART":
            tense = "past"
        elif node.getAttribute("tense") == "PRESPART":
            tense = "present"
        elif node.getAttribute("tense") == "NONE" or node.getAttribute("tense") == "INFINITIVE":
            tense = None
        else:
            tense = node.getAttribute("tense").lower()
        out_str+=value+str(node.childNodes[0].nodeValue) + "\t" + str(word_i) + "\t"
        if tense:
            out_str+=str(tense)
            if node.hasAttribute("aspect") and node.getAttribute("aspect")!="NONE":
                out_str += ("\t" + node.getAttribute("aspect"))
        out_str+="\n"
        return out_str

    def parse_text_data(value,word_i,out_str):

        _word_i = word_i
        while _word_i<len(words_tok) and value.find(words_tok[_word_i].decode("utf8")) == 0:
            out_str+= words_tok[_word_i] + "\t" + str(_word_i) + "\t" + "\n"
            value = value[len(words_tok[_word_i]):]
            _word_i += 1

        return _word_i,value,out_str

    generate_clean_articles(prefix)

    for root, _, files in os.walk(prefix + "\\" + DATA):
        for f in files:
            tense_format = open(prefix +  "\\" +  TENSE_FORMAT + "\\" + f,"w")
            fullpath = os.path.join(root, f)
            sentences =  get_sentences_nodes(fullpath)
            for sent_id, sent in zip(range(0,len(sentences)),sentences):
                value = ""
                out_str = ""
                sent_fn = prefix + "\\"+ UNMARKED_ARTICLES +"\\" + f + "." + str(sent_id)
                words_tok = tokenize(sent_fn)
                print words_tok

                word_i = 0
                for node in sent.childNodes:
                    if node.nodeType == node.ELEMENT_NODE and node.nodeName == "EVENT" and node.hasAttribute("tense") and node.hasAttribute("pos") and node.getAttribute("pos")=="VERB":
                                out_str = parse_tense_data(node,out_str,value)
                                word_i += 1
                    else:
                        if node.nodeType == node.TEXT_NODE:
                            value += "".join(node.nodeValue.split())
                        else:
                            value += "".join(node.childNodes[0].nodeValue.split())
                        word_i,value,out_str = parse_text_data(value,word_i,out_str)
                if value!="":
                    print "ERROR\t0\n\n"
                    tense_format.write("ERROR\t0\n\n")
                    os.remove(sent_fn)
                else:
                    tense_format.write(out_str + "\n")


generate_tense_format(TEMPEVAL_TRAINING)

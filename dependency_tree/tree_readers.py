__author__ = 'jessica'


import os
from dependency_tree.tree import *

# Input :   file path of constituency trees
# Output:   stream of the trees converted to dep trees
def convert_to_dep_tree(constituency_tree_fn):
   dir_path = os.path.dirname(os.path.abspath(__file__))
   convert_command = "java -cp " + dir_path +"/stanford_parser/stanford-parser.jar edu.stanford.nlp.trees.EnglishGrammaticalStructure -treeFile "+ constituency_tree_fn + " -conllx -basic -makeCopulaHead -keepPunct"
   stream = os.popen(convert_command)
   return stream


# Input :   stream of dep trees converted bt Stanford parser
# Output:   List of DepTree
def create_dep_trees_from_stream(stream):

    dep_trees = []
    init_flag = True
    token_id = 0

    for line in stream:
       line = line.strip()
       # Starting parsing of new tree
       if init_flag:
           dep_trees_data = {0:[]}
           dep_trees_nodes = {0:DepTree(pos="",word="ROOT",id=0,parent=None,parent_relation="",children=[])}
           init_flag = False

       # Create DepTree for node in dep tree
       if line != "" :
           node = line.split()
           id = int(node[0])
           dep_trees_data[id]=node
           dep_trees_nodes[id]=DepTree(pos=node[3],word=node[1],id=node[0],parent=None,parent_relation=node[7],children=[])
           token_id += 1

       # Here all tree nodes are already parsed
       else:
           # Going through all nodes and update connections between them
           for i in filter(lambda x:x,dep_trees_nodes.keys()):
               node_data = dep_trees_data[i]
               node = dep_trees_nodes[i]
               parent_id = int (node_data[6])
               # Set node's parent
               node.set_parent(dep_trees_nodes[parent_id])
               # Set node's parent id
               node.set_parent_id(parent_id)
               # Set the node to the child list of the parent
               dep_trees_nodes[parent_id].add_child(node)
               
           # Add parsed DepTree to the list
           dep_trees_nodes[0].n_tokens = token_id
           token_id = 0
           dep_trees.append(dep_trees_nodes[0])
           # Mark for initialization for parsing the next tree
           init_flag = True

    return dep_trees


def read_trees_file(constituency_tree_fn):
   stream = convert_to_dep_tree(constituency_tree_fn)
   return create_dep_trees_from_stream(stream)




__author__ = 'jessica'

from dependency_tree.definitions import *

UNDERSCORE = "_"

# DepTree is a class representing a dependency tree
class DepTree(object):

    def __init__(self,pos,word,id,parent=None,parent_id = None,parent_relation=None,children=[]):
        self.children = children                        # List of node's children
        self.parent = parent                            # Node's parent
        self.parent_relation = parent_relation          # Node's parent relation
        self.parent_id = parent_id                      # Node's parent id
        self.pos = pos                                  # pos tag
        self.word = word                                # word from sentence
        self.id = int(id)                               # location in sentence



    def set_parent(self, new_parent): self.parent = new_parent
    def set_parent_id(self,parent_id): self.parent_id = parent_id
    def get_parent(self): return self.parent
    def get_word(self): return self.word
    def get_pos(self): return self.pos
    def add_child(self,child): self.children.append(child)
    def get_children(self): return self.children
    def get_parent_relation(self): return self.parent_relation


    def __str__(self):
        if not self.children : return ""
        str = ""
        for child in self.children:
            str += "%s(%s,%s)\n%s" % (child.get_parent_relation(), self.word,child.get_word() ,child)
        return str

    # return list of nodes that satisfy predicate
    def search(self, predicate):
        if predicate(self):
            yield self
        for c in self.children:
            for res in c.search(predicate):
                yield res

  # get the original sentence from the PTB
    def get_original_sentence(self, root=True):
        if root:
            subtree = self.children[0]._get_subtree()
        else:
            subtree = self._get_subtree()
        return " ".join(subtree[x] for x in sorted(subtree))

    # return rooted subtree word dictionary by self.id
    def _get_subtree(self):
        ret = {self.id:self.word}
        if not self.children: return ret
        for child in self.children:
            ret.update(child._get_subtree())
        return ret

    # return rooted subtree word dictionary by self.id
    def _get_subtree_nodes(self,includeHead = False):
        def inner(node):
            ret = {node.id:node}
            for child in node.children:
                ret.update(inner(child))
            return ret
        d = inner(self)
        if not includeHead: d.pop(self.id)
        return d

    # return True if the node is a predicate
    def is_predicate(self):
        if self.is_verbal_predicate():
            return True
        return False

    # returns True if the node is a verbal predicate : (1) verb POS tag (2) not auxiliary verb
    def is_verbal_predicate(self):
        if self.pos.find(VB) != 0:
        #if self.pos != VB:
            return False
        #if self.parent_relation in aux_cop_dependencies:
        #    return False
        return True

    # returns  list of the verbal predicates in subtree
    def collect_verbal_predicates(self):
        if self.is_verbal_predicate():
            yield self
        for child in self.children:
            for node in child.collect_verbal_predicates():
                yield node

    # filter node's children according to the given function
    # returns (True/False, span) : True/False indicates if the node has children after the filter.
    #                              span indicates the filtered children min and max indexes
    def _get_span_of_filtered_children(self, child_func):
        nodes = filter(lambda x:child_func(x), self.children)
        if nodes == []:
            return False,(-1,-1)
        ids = [x.id for x in nodes]
        min_id,max_id = (min(ids),max(ids))
        return  True,(min_id,max_id)


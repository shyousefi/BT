import ast

class DependencyTree:

    def __init__(self):
        self._nodes = []
        self._max_modifier = 0
        self._max_mod_node = -1
        self._max_weight = 0
        self._max_weight_node = -1
        self._sum_weight = 0


    def _add_modifier(self, head: int, modifier: int):
        head_node = self._nodes[head]
        head_node.add_modifier(modifier)
        length = len(head_node.modifier())
        if length > self._max_modifier:
            self._max_modifier = length
            self._max_mod_node = head

    
    def _create_node(self,value: str, head: int, modifier: int, relation: str):
        weight = abs(head - modifier)
        if weight > self._max_weight:
            self._max_weight = weight
            self._max_weight_node = modifier
        self._sum_weight += weight
        node = Node(value, head, weight, relation)
        self._nodes += [node]


    def from_ud_sentence(self, sentence):
        assert self._nodes == []

        root = Node("root", None, 0, None)
        self._nodes += [root]
        
        lines = sentence.split("\n")
        tups = []
        for line in lines[:-1]:
            tup = tuple(line.split("\t"))
            tups += [tup]
            self._create_node(tup[1], int(tup[6]), int(tup[0]), tup[7])
        for tup in tups:
            self._add_modifier(int(tup[6]), int(tup[0]))

    
    def from_tp_sentence(self, sentence):
        assert self._nodes == []

        root = Node("root", None, 0, None)
        self._nodes += [root]

        lines = sentence.split("\n")
        tups = []
        for line in lines:
            if not line.startswith("("):
                continue
            tup = ast.literal_eval(line)
            tups += [tup]
            self._create_node(tup[1], int(tup[2]), int(tup[0]), tup[3])

        for tup in tups:
            self._add_modifier(int(tup[2]), int(tup[0]))


    def __getitem__(self, i):
        return self._nodes[i]


    def __len__(self):
        return len(self._nodes)


    def __iter__(self):
        return iter(self._nodes)


    def __contains__(self, node):
        return node in self._nodes


    def max_modifier(self):
        return self._max_modifier


    def max_mod_node(self):
        return self._max_mod_node


    def max_weight(self):
        return self._max_weight

    
    def max_weight_node(self):
        return self._max_weight_node

    
    def sum_weight(self):
        return self._sum_weight

    
    def get_mod_list(self):
        modifier = []
        for x in self._nodes:
            ls = x.modifier()
            modifier += [len(ls)]
        return modifier


class Node:

    def __init__(self, value: str, head: int, weight: int, relation: str):
        self._value = value
        self._head = head
        self._modifier = []
        self._weight = weight
        self._relation = relation
    

    def add_modifier(self, node: int):
        self._modifier += [node]


    def head(self):
        return self._head

    
    def value(self):
        return self._value

    
    def weight(self):
        return self._weight

    
    def relation(self):
        return self._relation

    
    def modifier(self):
        return self._modifier
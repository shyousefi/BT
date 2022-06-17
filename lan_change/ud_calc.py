import re
from tree import DependencyTree

def _read_conll(in_path):
    with open(in_path, "r") as reader:
        sentences = []
        sent = ""
        for line in reader:
            if line == "\n":
                if not sent:
                    continue
                sentences += [sent]
                sent = ""
                continue
            if line == "#" or not re.match("^\d+\.?\t", line):
                continue
            sent = sent + line
        if sent:
            sentences += [sent]
        return sentences            
            

def _calc_dm


def calc(in_path, out_path):
    sentences = _read_conll(in_path)
    dep_trees = []
    for sentence in sentences:
        dep_tree = DependencyTree()
        dep_tree.from_ud_sentence(sentence)
        dep_trees += [dep_tree]
    
    res_json = []
    max_dlm = 0
    max_norm = 0
    for i, dep_tree in enumerate(dep_trees):
        length = len(dep_tree)
        mean_dlm = dep_tree.sum_weight() / length
        root_node = dep_tree[0]
        root_modifier = dep_tree[root_node.modifier()[0]]
        root_dist = root_modifier.weight()
        norm_dlm = abs(math.log(mean / math.sqrt(root_dist*length)))



            
            
            
from itertools import cycle
import re
from tree import DependencyTree, Node
import math
import json
import numpy as np


def _read_tp(in_path):
    with open(in_path, "r") as reader:
        sentences = []
        sent = ""
        for line in reader:
            if line == "\n":
                if not sent:
                    continue
                sentences += [sent]
                sent = ""
            if line[0] != "(":
                continue
            sent = sent + line
        if sent:
            sentences += [sent]
        return sentences


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
            if line[0] == "#" or not re.match("^\d+\.?\t", line):
                continue
            sent = sent + line
        if sent:
            sentences += [sent]
        return sentences            
            

#https://www.geeksforgeeks.org/detect-cycle-in-a-graph/
def _has_cycle_util(tree, v, visited, recStack):
        visited[v] = True
        recStack[v] = True
        for neighbour in tree[v].modifier():
            if visited[neighbour] == False:
                if _has_cycle_util(tree, neighbour, visited, recStack) == True:
                    return True
            elif recStack[neighbour] == True:
                return True
 
        recStack[v] = False
        return False


def _has_cycle(tree: DependencyTree):
    visited = [False] * len(tree)
    recStack = [False] * len(tree)
    for i, node in enumerate(tree):
        if visited[i] == False:
            if _has_cycle_util(tree,i,visited,recStack) == True:
                return True
    return False

def _get_depth(tree: DependencyTree, index: int):
    h = 0
    try:
        for i in tree[index].modifier():    
            h = max(h, _get_depth(tree, i))
    except:
        exit()
    return h + 1


def _process_files(in_path: str, tp: bool):
    dep_trees = []
    if tp:
        sentences = _read_tp(in_path)
        for sentence in sentences:
            dep_tree = DependencyTree()
            dep_tree.from_tp_sentence(sentence)
            dep_trees += [dep_tree]
    else:
        sentences = _read_conll(in_path)
        for sentence in sentences:
            dep_tree = DependencyTree()
            dep_tree.from_ud_sentence(sentence)
            dep_trees += [dep_tree]
    return dep_trees


def _get_dates(date_path):
    deuparl_dates = {1: 1953, 2: 1957, 3: 1961, 4: 1965, 5: 1969, 6: 1972, 7: 1976, 8: 1980, 9: 1983, 10: 1987, 11: 1990, 12: 1994, 13: 1998, 14: 2002, 16: 2005, 17: 2009, 18: 2017, 19: 2020}
    with open(date_path, "r") as file:
        data = json.load(file)
        dates = [date["date"] for date in data]
        if "DeuParl" in date_path:
            dates = [deuparl_dates.get(int(date), date) for date in dates]
        return dates


def write_measurements(in_path, date_path, out_path, tp=False):
    dep_trees = _process_files(in_path, tp)
    dates = _get_dates(date_path)
    tree_data = []
    cycles = []
    max_length = 0
    max_degree = 0
    max_dlm = 0
    max_norm = 0
    max_height = 0
    sum_degrees = 0
    for i, dep_tree in enumerate(dep_trees):
        root_node = dep_tree[0]
        has_cycle = _has_cycle(dep_tree)
        if has_cycle:
            cycles += [i]
            continue
        if not root_node.modifier():
            continue
        entry = {}
        length = len(dep_tree)
        entry["length"] = length
        if length > max_length:
            max_length = length
        mean_dlm = dep_tree.sum_weight() / length
        entry["mean_dlm"] = mean_dlm
        if mean_dlm > max_dlm:
            max_dlm = 0
        root_modifier = dep_tree[root_node.modifier()[0]]
        root_dist = root_modifier.weight()
        entry["root_dist"] = root_dist
        norm_dlm = abs(math.log(mean_dlm / math.sqrt(root_dist*length)))
        entry["norm_dlm"] = norm_dlm
        if norm_dlm > max_norm:
            max_norm = norm_dlm
        max_modifier = dep_tree.max_modifier()
        entry["max_degree"] = max_modifier
        if max_modifier > max_degree:
            max_degree = max_modifier
        entry["largest_sing_dist"] = dep_tree.max_weight()
        root_height = -1
        root_height = _get_depth(dep_tree, 0)
        entry["root_height"] = root_height
        norm_height = root_height/math.ceil(math.log(length))
        entry["norm_height"] = norm_height
        if norm_height > max_height:
            max_height = norm_height
        max_degree_node_height = 0
        max_degree_node_height = _get_depth(dep_tree, dep_tree.max_mod_node())
        entry["max_dn_height"] = max_degree_node_height
        try:
            date = dates[i]
        except:
            print(in_path)
            print(i)
            print(len(dep_trees))
            print(dates)
            exit()
        if "-" in str(dates[i]):
            date = date.split("-")[0]
        entry["date"] = int(date)
        in_degrees = np.array(dep_tree.get_mod_list())
        in_degree_var = np.var(in_degrees)
        comp_tree = np.zeros(length)
        comp_tree[0] = length - 1
        normed_degree_var = in_degree_var / np.var(comp_tree)
        entry["in_degree_var"] = normed_degree_var
        dep_rels = {}
        for i, node in enumerate(dep_tree):
            val = node.weight()
            if val == 0:
                continue
            key = node.relation()
            deg = len(node.modifier())
            height = _get_depth(dep_tree, i)
            if key in dep_rels.keys():
                dep_rels[key]["dlm"] += [val]
                dep_rels[key]["degree"] += [deg]
                dep_rels[key]["height"] += [height]
            else:
                dep_rels[key] = {"dlm": [val], "degree": [deg], "height": [height]}
        entry["dep_rels"] = dep_rels
        crossings = []
        for j, node in enumerate(dep_tree):
            for edge in node.modifier():
                for k, n in enumerate(dep_tree):
                    if j == k or edge == k:
                        continue
                    for e in n.modifier():
                        if edge == e or e == j:
                            continue
                        u = j if j < edge else edge
                        v = j if j > edge else edge
                        x = k if k < e else e
                        y = k if k > e else e
                        if (u, v, x, y) in crossings or (x, y, u, v) in crossings:
                            continue
                        if u < x < v < y:
                            crossings += [(u, v, x, y)]
                            continue
                        if x < u < y < v:
                            crossings += [(x, y, u, v)]
        entry["crossings"] = len(crossings)
        entry["normed_cross"] = len(crossings)/(((length-1) * (length-2))/2)
        inserted = False
        for i, e in enumerate(tree_data):
            if e["date"] > int(date):
                tree_data.insert(i, entry)
                inserted = True
                break
        if not inserted:
            tree_data += [entry]
    res_json = {}
    res_json["data"] = tree_data
    res_json["max_length"] = max_length
    res_json["max_degree"] = max_degree
    res_json["max_dlm"] = max_dlm
    res_json["max_norm"] = max_norm
    res_json["max_height"] = max_height
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(res_json, f, ensure_ascii=False, indent=4)
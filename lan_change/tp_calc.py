import ast
import json
import math

from torch import norm_except_dim

def calc(in_path: str, out_path: str):
    data = []
    avg_length = 0
    avg = 0
    max_val = 0
    avg_norm = 0
    max_norm = 0
    with open(in_path, "r") as reader:
        text = reader.read()
        sentences = text.split("\n\n")
        for sentence in sentences:
            if not sentence:
                continue
            sum = 0
            lines = sentence.split("\n")
            root_dist = 1
            for line in lines:
                if not line.startswith("("):
                    continue
                try:
                    t = ast.literal_eval(line)
                except e:
                    print(e)
                    exit()
                dist = abs(int(t[0]) - int(t[2]))
                if t[2] == 0:
                    root_dist = dist
                sum += dist
            last_line = lines[-1]
            length = int(ast.literal_eval(last_line)[0])
            mean = sum / length
            norm = abs(math.log(mean / math.sqrt(root_dist*length)))
            entry = {"length": length, "dep_length" : sum, "mean": mean, "norm": norm}
            data = data + [entry]
            avg_length += length
            avg += mean
            avg_norm += norm
            if max_val < mean:
                max_val = mean
            if max_norm < norm:
                max_norm = norm
        avg /= len(sentences)
        avg_length /= len(sentences)
        avg_norm /= len(sentences)
    dlm = {"data": data, "average_length": avg_length, "average_dep": avg, "max_dep": max_val, "average_norm": avg_norm, "max_norm": max_norm}
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(dlm, f, ensure_ascii=False, indent=4)
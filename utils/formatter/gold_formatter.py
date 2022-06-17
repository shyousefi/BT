import os

gold_data_path = "/ukp-storage-1/krause/Thesis/results/trainning_sets/gold"

def is_conllu_line(sentence):
    return sentence.count("\t") == 9 or sentence.count("\t") == 10


def remove_cycles(sentence):
    if is_conllu_line(sentence):
        tokens = sentence.split("\t")
        head_index = tokens[6]
        sent_index = tokens[0]
        if head_index == sent_index:
            tokens[6] = "0"
            new_sent = "\t".join(tokens)
            print(new_sent)
            return new_sent
    return sentence


def comment_wrong_lines(sentence):
    if not sentence or sentence.count("\t") == 9 or sentence.count("\t") == 10 or sentence[0] == "#"  or sentence[0] == "\n":
        return sentence
    return "#" + sentence


def to_root(sentence):
    if is_conllu_line(sentence):
        tokens = sentence.split("\t")
        if (tokens[6] == "0" and tokens[7] == "--") or (tokens[7] == "ROOT") :
            tokens[7] = "root"
            return "\t".join(tokens)
    return sentence


for directory in os.listdir(gold_data_path):
    dir_path = os.path.join(gold_data_path, directory)
    for conllu in os.listdir(dir_path):
        conllu_path = os.path.join(dir_path, conllu)
        if not conllu.endswith(".conllu"):
            continue
        text = ""
        with open(conllu_path, "r") as reader:
            for line in reader:
                new_line = remove_cycles(line)
                new_line = to_root(new_line)
                new_line = comment_wrong_lines(new_line)
                text = text + new_line
        with open(conllu_path, "w") as writer:
            writer.write(text)
        
import os
from tower import TowerParser

gold_data = "/ukp-storage-1/krause/Thesis/data/training_few_shot"
model_path = "/ukp-storage-1/krause/Thesis/data/gsd/UD_German-GSD"
out_path = "/ukp-storage-1/krause/Thesis/results/towerparse/eval"
parser = TowerParser(model_path)
lan = "en" if model_path.lower().__contains__("english") else "de"

def evaluate(tokens, heads, dep):
    sentences = parser.parse(lan, [tokens])
    correct_head = 0
    correct_dep = 0
    for ps in sentences:
        for i in range(len(ps)):
            if int(heads[i]) == ps[i][2]:
                correct_head += 1
            if dep[i].lower() == ps[i][3].lower():
                correct_dep += 1
    return correct_head, correct_dep


if __name__ == "__main__":
    for conllu in os.listdir(gold_data):
        if not conllu.__contains__(lan):
            continue
        if not conllu.endswith(".conllu"):
            continue
        conllu_path = os.path.join(gold_data, conllu)
        count = 0
        total_cor_heads = 0
        total_cor_deps = 0
        with open(conllu_path, "r") as reader:
            is_sentence = False
            tokens = []
            heads = []
            dep = []
            for line in reader:
                if not line or line[0] == "#" or (not is_sentence and line == "\n"):
                    continue
                if line == "\n":
                    cor_heads, cor_deps = evaluate(tokens, heads, dep)
                    total_cor_heads += cor_heads
                    total_cor_deps += cor_deps
                    is_sentence = False
                    tokens = []
                    heads = []
                    dep = []
                    continue
                is_sentence = True
                parts = line.split("\t")
                count += 1
                try:
                    tokens = tokens + [parts[1]]
                except:
                    print(line)
                    print(parts)
                heads = heads + [parts[6]]
                dep = dep + [parts[7]]
            eval_file = os.path.join(out_path, conllu + ".txt")
            with open(eval_file, "w") as writer:
                uas = total_cor_heads / count
                las = total_cor_deps / count
                writer.write("UAS: " + str(uas) + "\n")
                writer.write("LAS: " + str(las) + "\n")
                writer.write("Tokens: " + str(count))

import os
import random
from pathlib import Path


#"/ukp-storage-1/krause/Thesis/data/DeuParl/extracted_random",
#           "/ukp-storage-1/krause/Thesis/data/COHA/extracted_sentences/random"
in_paths = ["/ukp-storage-1/krause/Thesis/data/Hansard/extracted_sentences/new"]
#["/ukp-storage-1/krause/Thesis/data/Hansard/extracted_sentences/random", "/ukp-storage-1/krause/Thesis/data/DeuParl/extracted_random", "/ukp-storage-1/krause/Thesis/data/COHA/extracted_sentences/random"]
result_path = "/ukp-storage-1/krause/Thesis/results/extracted_sentences"

HANSARD = "Hansard"
DEUPARL = "DeuParl"
COHA = "COHA"
seed = 1337


def get_out_path(in_path):
    if in_path.lower().__contains__(HANSARD.lower()):
        return os.path.join(result_path, HANSARD + "_new")
    elif in_path.lower().__contains__(DEUPARL.lower()):
        return os.path.join(result_path, DEUPARL + "_new")
    return os.path.join(result_path, COHA)

random.seed(seed)

for path in in_paths:
    for txt in os.listdir(path):
        txt_path = os.path.join(path, txt)
        with open(txt_path, "r") as reader:
            text = reader.read()
            sentences = text.split("\n")
            random.shuffle(sentences)
            base_path = get_out_path(path)
            Path(base_path).mkdir(parents=True, exist_ok=True)
            out_path = os.path.join(base_path, txt)
            with open(out_path, "w") as writer:
                amount = 50 if path.__contains__(DEUPARL) else 50
                for i in range(amount):
                    writer.write(sentences.pop())
                    writer.write("\n")



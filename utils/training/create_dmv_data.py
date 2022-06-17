import os
import re
from pathlib import Path

conllu_path = "/ukp-storage-1/krause/Thesis/results/training_sets/ger_gsd_few_shot"
out_path = "/ukp-storage-1/krause/Thesis/results/training_sets/ger_gsd_few_shot"

Path(out_path).mkdir(parents=True, exist_ok=True)
for conllu in os.listdir(conllu_path):
    if not conllu.endswith(".conllu"):
        continue
    file_path = os.path.join(conllu_path, conllu)
    text = ""
    with open(file_path, "r") as reader:
        for line in reader:
            match = re.match("^\d+(-|\.)\d+", line)
            if match:
                continue
            text = text + line
    out_file = ""
    if conllu.__contains__("train"):
        out_file = "train.conllu"
    elif conllu.__contains__("test"):
        out_file = "test.conllu"
    else:
        out_file = "dev.conllu"
    result_path = os.path.join(out_path, out_file)
    with open(result_path, "w") as writer:
        writer.write(text)


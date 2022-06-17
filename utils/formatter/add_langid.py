import os
from pathlib import Path

data_path = "/ukp-storage-1/krause/Thesis/results/crfpar"
corpora = ["COHA", "Hansard", "DeuParl"]
dirs = ["modern"]
out_base_path = "/ukp-storage-1/krause/Thesis/data/udapter"

for corpus in corpora:
    lan = "de" if corpus.__contains__("DeuParl") else "en"
    for directory in dirs:
        relative_path = os.path.join(corpus, directory)
        directory_path = os.path.join(data_path, relative_path)
        for conllu in os.listdir(directory_path):
            if not conllu.endswith(".conllu"):
                continue
            conllu_path = os.path.join(directory_path, conllu)
            text = ""
            with open(conllu_path, "r") as reader:
                for line in reader:
                    if line[0] == "\n" or line[0] == "#":
                        text = text + line
                    else:
                        new_line = line.replace("\n", "") + "\t" + lan + "\n"
                        text = text + new_line
                reader.close()

            result_dir = os.path.join(out_base_path, relative_path)
            Path(result_dir).mkdir(exist_ok=True, parents=True)
            result_conllu = os.path.join(result_dir, conllu)
            with open(result_conllu, "w") as writer:
                writer.write(text)
                writer.close()
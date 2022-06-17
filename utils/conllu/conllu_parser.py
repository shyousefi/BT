import os
from pathlib import Path


coha_dir = "/ukp-storage-1/krause/Thesis/data/Hansard/extracted_sentences/random"
out_dir = "/ukp-storage-1/krause/Thesis/data/Hansard/conllu"
lang = "en"

Path(out_dir).mkdir(parents=True, exist_ok=True)
for txt in os.listdir(coha_dir):
    txt_path = os.path.join(coha_dir, txt)
    with open(txt_path, "r") as reader:
        for line in reader:
            words = line.replace("\n", "").split(" ")
            new_lines = []
            for i in range(len(words)):
                new_line = str(i+1) + "\t" + words[i] + "\t"
                for j in range(8):
                    new_line = new_line + "-\t"
                new_line = new_line + lang + "\n"
                new_lines = new_lines + [new_line]
            with open(os.path.join(out_dir, txt.replace(".txt", ".conllu")), "a") as writer:
                writer.writelines(new_lines)
                writer.write("\n")
                writer.close()
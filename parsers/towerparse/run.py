from tower import TowerParser
import nltk
import os
from pathlib import Path


def write_parsed(parsed_sents, dest):
    with open(dest, "a") as writer:
        for ps in parsed_sents:
            for token in ps:
                writer.write(str(token))
                writer.write("\n")
            writer.write("\n")


out_path = "/ukp-storage-1/krause/Thesis/results/towerparse/DeuParl"
in_path = "/ukp-storage-1/krause/Thesis/data/DeuParl/extracted_sentences/with_dates"
model_path = "/ukp-storage-1/krause/Thesis/data/gsd/UD_German-GSD"
parser = TowerParser(model_path)

Path(out_path).mkdir(exist_ok=True, parents=True)
for file in os.listdir(in_path):
    if not file.endswith(".txt"):
        continue
    n = int(file.split("-")[0])
    if n != 6 and n != 5:
        continue
    path = os.path.join(in_path, file)
    with open(path, "r") as reader:
        for line in reader:
            words = [nltk.word_tokenize(line)]
            try:
                parsed_en = parser.parse("en", words)
            except IndexError as e:
                print(e)
                continue
            write_parsed(parsed_en, os.path.join(out_path, file))
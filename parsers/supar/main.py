from supar import Parser
import os
import gc
import torch
from pathlib import Path

model_path = "/ukp-storage-1/krause/Thesis/parsers/supar/trained_models/ger.txt"
data_paths = ["/ukp-storage-1/krause/Thesis/data/DeuParl/extracted_sentences/with_dates"]
#["/ukp-storage-1/krause/Thesis/data/COHA/extracted_sentences/random", "/ukp-storage-1/krause/Thesis/data/Hansard/extracted_sentences/random"]
save_paths = ["/ukp-storage-1/krause/Thesis/results/crfpar/DeuParl/modern"]#["/ukp-storage-1/krause/Thesis/results/crfpar/DeuParl"]

def get_save_path(path):
    corpora = ["COHA", "Hansard", "DeuParl"]
    for corpus in corpora:
        if path.__contains__(corpus):
            for save_path in save_paths:
                if (save_path.__contains__(corpus)):
                    Path(save_path).mkdir(parents=True, exist_ok=True)
                    return save_path
    return None

parser = Parser.load(model_path)


for data_path in data_paths:
    for file in os.listdir(data_path):
        if not file.endswith(".txt"):
            continue
        n = int(file.split("-")[0])
        if n != 6 and n != 5:
            continue
        path = os.path.join(data_path, file)
        save_path = get_save_path(data_path)
        lang = "de" if save_path.__contains__("DeuParl") else "en"
        if not save_path:
            continue
        with open(path, "r") as reader:
            for line in reader:
                dataset = parser.predict(line, lang=lang, prob=True, verbose=False)
                gc.collect()
                torch.cuda.empty_cache()
                out_path = os.path.join(save_path, file.replace(".txt", ".conllu"))
                with open(out_path, "a") as writer:
                    writer.write(str(dataset[0]))
                    writer.write("\n")
                    writer.close
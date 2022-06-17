import os
import meassure

tp_path = "/ukp-storage-1/krause/Thesis/results/towerparse"
crf_path = "/ukp-storage-1/krause/Thesis/results/crfpar"
ud_path = "/ukp-storage-1/krause/Thesis/results/udapter"
date_path = "/ukp-storage-1/krause/Thesis/data/{}/extracted_sentences/with_dates"
corpora = ["COHA","DeuParl","Hansard"]


def _go_into_corpus(corpus_path):
    for file in os.listdir(corpus_path):
        path_to_file = os.path.join(corpus_path, file)
        if not (file.endswith(".txt") or file.endswith(".conllu") or os.path.isdir(path_to_file)):
            continue
        if file.startswith("mk_"):
            continue
        if os.path.isdir(path_to_file):
            _go_into_corpus(path_to_file)
        else:
            corpus = ""
            for c in corpora:
                if c.lower() in corpus_path.lower():
                    corpus = c
            in_path = os.path.join(corpus_path, file)
            json_name = file.replace(".txt", ".json")
            json_name = json_name.replace(".conllu", ".json")
            out_path = os.path.join(corpus_path, json_name)
            d = date_path.format(corpus)
            d_path = os.path.join(d, json_name)
            if "towerparse" in in_path:
                meassure.write_measurements(in_path, d_path, out_path, True)
            else:
                meassure.write_measurements(in_path, d_path, out_path)
                continue


def analyze(path):
    for directory in os.listdir(path):
        if directory == "eval":
            continue
        corpus_path = os.path.join(path, directory)
        _go_into_corpus(corpus_path)
               


def main():
    #analyze(tp_path)
    #analyze(crf_path)
    analyze(ud_path)


if __name__ == '__main__':
    main()
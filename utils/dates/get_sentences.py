import json
import os

gold_sentences = ["/ukp-storage-1/krause/Thesis/data/gold/de.conllu", "/ukp-storage-1/krause/Thesis/data/gold/en.conllu"]
out_dir = ""


def main():
    for conllu in gold_sentences:
        text = []
        with open(conllu, "r") as reader:
            for line in reader:
                if not line.startswith("# text"):
                    continue
                text += [line.replace("\n", "").replace("# text = ", "")]
        file = conllu.split("/")[-1].replace(".conllu", ".json")
        out_path = os.path.join(out_dir, file)
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(text, f, ensure_ascii=False, indent=4)   

if __name__ == "__main__":
    main()
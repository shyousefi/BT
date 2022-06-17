import json
import os

gold_sentences = ["en.json"]
txt = "/ukp-storage-1/krause/Thesis/utils/dates/hansard.txt"
out_dir = ""


def main():
    for json_file in gold_sentences:
        text = []
        with open(json_file, 'r') as f:
            data = json.load(f)
        with open(txt, "r") as reader:
            text = reader.read()
        i = 0
        while i < len(data):
            if data[i] in text:
                del data[i]
                continue
            i +=1
        out_path = os.path.join(out_dir, "en_distinct.json")
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)   

if __name__ == "__main__":
    main()
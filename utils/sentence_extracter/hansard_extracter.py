import os
import nltk
import pandas as pd
from pathlib import Path
import re
import string
import heuristics
import random
import json

base_dir = "/ukp-storage-1/krause/Thesis/data/Hansard/"
hansard_dir = os.path.join(base_dir, "csv")
sentences_dir = os.path.join(base_dir, "extracted_sentences/with_dates")
seed = 1337

def is_year(x):
    return re.match("(1[7-9]|2[0-2])\d\d($|\.|\n)", x)


Path(sentences_dir).mkdir(parents=True, exist_ok=True)
print(sentences_dir)
random.seed(seed)
for csv in os.listdir(hansard_dir):
    if csv.endswith(".csv"):
        csv_path = os.path.join(hansard_dir, csv)
        df = pd.read_csv(csv_path, sep="\t", usecols=["debates", "date"])
        tups = [tuple(row) for row in df.values]
        amount_of_sentences = 1000
        texts = []
        dates = []
        for tup in tups:
            debate = tup[0]
            date = tup[1]
            try:
                debs_tokenized = nltk.sent_tokenize(debate)
                texts += debs_tokenized
                dates += len(debs_tokenized) * [date]
            except:
                continue

        res_json = []
        while texts and amount_of_sentences > 0:
            index = random.choice(range(0, len(texts)))
            sentence = texts[index]
            date = dates[index]
            del texts[index]
            del dates[index]
            tokenized_text = nltk.word_tokenize(sentence)
            tokenized_text = list(filter(lambda x: not str.isdigit(x) and not is_year(x), tokenized_text))
            if not heuristics.is_hansard_sentence_correct(sentence, tokenized_text):
                continue
            new_sentence = ""
            for word in tokenized_text:
                if not string.punctuation.__contains__(word):
                    new_sentence = new_sentence + " "
                new_sentence = new_sentence + word
            with open(os.path.join(sentences_dir,  csv.replace(".csv", ".txt")), "a") as f:
                f.write(new_sentence[1:])
                f.write("\n")
                amount_of_sentences -= 1
            res_json += [{"sent": new_sentence[1:], "date": date}]
        with open(os.path.join(sentences_dir, csv.replace(".csv", ".json")), "w", encoding='utf-8') as f:
            json.dump(res_json, f, ensure_ascii=False, indent=4)  
            

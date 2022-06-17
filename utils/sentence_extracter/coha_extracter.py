from pathlib import Path
import os
import heuristics
import nltk
import string
import random
import re
import json

coha_dir = "/ukp-storage-1/krause/Thesis/data/COHA/unzipped"
sentences_dir = "/ukp-storage-1/krause/Thesis/data/COHA/extracted_sentences/with_dates"
seed = 1337


Path(sentences_dir).mkdir(parents=True, exist_ok=True)
random.seed(seed)
for period in os.listdir(coha_dir):
    period_path = os.path.join(coha_dir, period)
    texts = []
    dates = []
    for txt in os.listdir(period_path):
        txt_path = os.path.join(period_path, txt)
        with open(txt_path, "r") as reader:
            try:
                tokenized_sents = nltk.sent_tokenize(reader.read())
                texts += tokenized_sents
                date = re.search("_(\d{4})_", txt).group(1)
                dates += len(tokenized_sents) * [date]
            except:
                continue
    amount_of_sentences = 1000
    res_json = []
    while texts and amount_of_sentences > 0:
        index = random.choice(range(0, len(texts)))
        sentence = texts[index]
        date = dates[index]
        del texts[index]
        del dates[index]
        if sentence.__contains__("@"):
            continue
        tokenized_text = nltk.word_tokenize(sentence)
        if not heuristics.is_sentence_correct(tokenized_text):
            continue
        with open(os.path.join(sentences_dir,  period + ".txt"), "a") as f:
            f.write(sentence)
            f.write("\n")
            amount_of_sentences -= 1
        res_json += [{"sent": sentence, "date": date}]
    with open(os.path.join(sentences_dir, period + ".json"), "w", encoding='utf-8') as f:
        json.dump(res_json, f, ensure_ascii=False, indent=4)  
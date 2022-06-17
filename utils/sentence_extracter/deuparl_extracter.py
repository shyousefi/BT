import os
import nltk
import random
import heuristics
import string
import logging
from pathlib import Path
import json

deuparl_dir = "/storage/nllg/compute-share/bodensohn/deuparl/DeuParl/data/5_postprocessed"
extracted_sentences_dir = "/ukp-storage-1/krause/Thesis/data/DeuParl/with_dates"
seed = 1337

def check_period(time_period):
    if time_period.__contains__("SPD2") or time_period.__contains__("NS"):
        return 1000
    return 2000

def get_period(year):
    if 1890 > year >= 1867:
        return "1-KR1"
    elif 1918 > year >= 1890:
        return "2-KR2"
    elif 1933 > year >= 1918:
        return "3-WR"
    elif 1942 >= year >= 1933:
        return "4-NS"
    elif 5 >= year >= 1:
        return "5-CDU1"
    elif 9 >= year >= 6:
        return "6-SPD1"
    elif 13 >= year >= 10:
        return "7-CDU2"
    elif 15 >= year >= 14:
        return "8-SPD2"
    elif 19 >= year >= 16:
        return "9-CDU3"
    return ""


def extract(path):
    years = sorted(os.listdir(path), key= lambda x: int(x))
    start_period = "5-CDU1"
    last_period = start_period
    while years:
        sentences = []
        dates = []
        while years:
            year = years[0]
            curr_period = get_period(int(year))
            if curr_period != start_period:
                last_period = start_period
                start_period = curr_period
                break
            year_path = os.path.join(path, year)
            text = ""
            for text_slice in os.listdir(year_path):
                slice_path = os.path.join(year_path, text_slice)
                with open(slice_path, "r") as reader:
                    text = reader.read().strip()
                tokenized_sents = nltk.sent_tokenize(text)
                sentences += tokenized_sents
                dates += len(tokenized_sents) * [year]
            del years[0]
            print(year)
        amount_of_sentences = check_period(last_period)
        res_json = []
        while sentences and amount_of_sentences > 0:
            index = random.choice(range(0, len(sentences)))
            sentence = sentences[index]
            date = dates[index]
            del sentences[index]
            del dates[index]
            tokenized_sent = nltk.word_tokenize(sentence)
            if not heuristics.deuparl_is_sentence_correct(sentence, tokenized_sent):
                continue
            new_sentence = ""
            for word in tokenized_sent:
                if not string.punctuation.__contains__(word):
                    new_sentence = new_sentence + " "
                new_sentence = new_sentence + word
            print("writing")
            with open(os.path.join(extracted_sentences_dir, last_period + ".txt"), "a") as f:
                f.write(new_sentence[1:])
                f.write("\n")
                amount_of_sentences -= 1
            res_json += [{"sent": new_sentence[1:], "date": date}]
        with open(os.path.join(extracted_sentences_dir, last_period + ".json"), "w", encoding='utf-8') as f:
            json.dump(res_json, f, ensure_ascii=False, indent=4)  


def main():
    Path(extracted_sentences_dir).mkdir(parents=True, exist_ok=True)
    random.seed(seed)
    bundestags_path = os.path.join(deuparl_dir, "Bundestag")
    reichstags_path = os.path.join(deuparl_dir, "Reichstag")
    extract(bundestags_path)
    #extract(reichstags_path)
    

if __name__ == "__main__":
    main()
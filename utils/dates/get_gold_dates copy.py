from dis import dis
from importlib.machinery import DEBUG_BYTECODE_SUFFIXES
import hansard_csv_reader
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import json
import string
import os
from numba import cuda
from numba import int64
from numba import jit
import numpy


deuparl_gold = "/ukp-storage-1/krause/Thesis/data/gold/de.conllu"
hansard_gold = "/ukp-storage-1/krause/Thesis/data/gold/en.conllu"

deuparl_dir = "/storage/nllg/compute-share/bodensohn/deuparl/DeuParl/data/3_ocr_post_corrected"

res_base = "/ukp-storage-1/krause/Thesis/utils/dates/"


#implementation from https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/

@cuda.jit(device=True)
def levenshtein_distance(sent1, sent2, distances):
    if sent1 and sent2:
        for t1 in range(len(sent1) + 1):
            distances[t1][0] = t1

        for t2 in range(len(sent2) + 1):
            distances[0][t2] = t2
            
        a = 0
        b = 0
        c = 0
        
        for t1 in range(1, len(sent1) + 1):
            for t2 in range(1, len(sent2) + 1):
                if sent1[t1-1]:
                    s1 = sent1[t1-1]
                if sent2[t2-1]:
                    s2 = sent2[t2-1]
                if (s1 is s2):
                    distances[t1][t2] = distances[t1 - 1][t2 - 1]
                else:
                    a = distances[t1][t2 - 1]
                    b = distances[t1 - 1][t2]
                    c = distances[t1 - 1][t2 - 1]
                    
                    if (a <= b and a <= c):
                        distances[t1][t2] = a + 1
                    elif (b <= a and b <= c):
                        distances[t1][t2] = b + 1
                    else:
                        distances[t1][t2] = c + 1

@cuda.jit
def compare(sentences, comp_sent, date, certain, certain_dates, uncertain, uncertain_dates, uncertain_sents, distances):
    i = cuda.grid(1)
    if i < len(sentences):
        sent = sentences[i]
        dist = distances[i]
        levenshtein_distance(sent, comp_sent, dist)
        d = dist[len(sent)][len(comp_sent)]
        certainty = 1 - (d / max(len(sent), len(comp_sent)))
        if certainty >= 0.8 and certain[i] < certainty:
            certain[i] = certainty
            certain_dates[i] = date
            uncertain[i] = -1
            uncertain_dates[i] = -1
            uncertain_sents[i] = ""
        elif certain[i] == -1 and certainty >= 0.5 and uncertain[i]["certainty"] < certainty:
            uncertain[i] = certainty
            uncertain_dates[i] = date
            uncertain_sents[i] = comp_sent


@jit
def create_matrix(sentences, deb_sent, matrix):
    for sent in sentences:
        matrix.append(numpy.zeros((len(sent) + 1,len(deb_sent) +1)))



def search_years(sentences, in_path, out_path):
    length = len(sentences)
    certain = [-1.0] * length
    certain_dates = [-1] * length
    uncertain = [-1.0] * length
    uncertain_dates = [-1] * length
    uncertain_sents = [""] * length
    for year in os.listdir(in_path):
        print(year)
        year_path = os.path.join(in_path, year)
        for f in os.listdir(year_path):
            file_path = os.path.join(year_path, f)
            with open(file_path, "r") as reader:
                for line in reader:
                    if len(line) < 7:
                        continue
                    threadsperblock = 32 
                    blockspergrid = (len(sentences) + (threadsperblock - 1)) // threadsperblock
                    distances = numpy.array([[[]]])
                    compare[blockspergrid, threadsperblock](sentences, line, year, certain, certain_dates, uncertain, uncertain_dates, uncertain_sents, distances)
                print(certain)
                print(certain_dates)
                print(uncertain)
                exit()
    data = {"certain": certain, "uncertain": uncertain, "left": sentences}
    write_data(out_path, data)
    return sentences            
        

def write_deuparl_dates():
    sentences = get_sentences(deuparl_gold)
    bundestag_dir = os.path.join(deuparl_dir, "Bundestag")
    bund_out = os.path.join(res_base, "bundestag.json")
    reichstag_dir = os.path.join(deuparl_dir, "Reichstag")
    reich_out = os.path.join(res_base, "reichstag.json")
    print("Checking Reichstag...")
    sentences = search_years(sentences, reichstag_dir, reich_out)
    print("Checking Bundestag...")
    sentences = search_years(sentences, bundestag_dir, bund_out)
    

def get_sentences(path):
    sentences = []
    with open(path, "r") as reader:
        sent = ""
        for line in reader:
            if line == "#":
                continue
            if line == "\n":
                if not sent:
                    continue
                sentences += [sent[1:]]
                sent = ""
                continue
            if "\t" not in line:
                continue
            word = line.split("\t")[1]
            if word in string.punctuation:
                sent = sent + word
            else:
                sent = sent + " " + word
        if sent:
            sentences += [sent]
    return sentences
            

def write_data(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)   


def write_hansard_dates():
    hansard = hansard_csv_reader.read()
    sentences = get_sentences(hansard_gold)
    certain = []
    uncertain = []
    for index, row in hansard.iterrows():
        if not sentences:
            break
        debates = row["debates"]
        if not isinstance(debates, str):
            continue
        try:
            deb_sents = sent_tokenize(debates)
            for deb_sent in deb_sents:
                i = 0
                while i < len(sentences):
                    if compare(sentences[i], deb_sent, row["date"], certain, uncertain):
                        del sentences[i]
                        continue
                    i += 1
        except Exception as e:
            print(e)
            continue
    data = {"certain": certain, "uncertain": uncertain, "left": sentences}
    write_data(os.path.join(res_base, "hansard_gold.json"), data)  


def main():
    print("Writing Hansard dates")
    #write_hansard_dates()
    print("Writing Deuparl dates")
    write_deuparl_dates()


if __name__ == "__main__":
    main()
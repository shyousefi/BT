vocab_path = "/ukp-storage-1/krause/Thesis/parsers/udapter/data/vocab/test/vocabulary/langs.txt"
oov_path = "/ukp-storage-1/krause/Thesis/parsers/udapter/languages/oov-langs.txt"
in_path = "/ukp-storage-1/krause/Thesis/parsers/udapter/languages/in-langs.txt"

vocabs = []
with open(vocab_path, "r") as reader:
    vocabs = reader.read().split("\n")

lan = []
with open(oov_path, "r") as reader:
    lan = reader.read().split("\n")

with open(in_path, "r") as reader:
    lan = lan + reader.read().split("\n")

for x in vocabs:
    if not lan.__contains__(x):
        print(x)
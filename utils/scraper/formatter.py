import nltk
from bs4 import BeautifulSoup
from nltk import tokenize
import zipfile
import csv

data_dir = "data/1803-1820/S1V0001P0.txt"
lol = "data/1803-1820/"
# for directory in os.listdir(data_dir):
#     zip_dir = data_dir + directory + "/"
#     for zip_file in os.listdir(zip_dir):
#         if zip_file.endswith(".zip"):
#             archive = zipfile.ZipFile(zip_dir + zip_file, "r")
#             for xml in archive.filelist:
#                 if xml.filename.endswith(".xml"):
#                     file = archive.read(xml.filename)
#                     soup = BeautifulSoup(file, "lxml")

# archive = zipfile.ZipFile(data_dir, "r")
# for xml in archive.filelist:
#     file = archive.read(xml.filename)
#     soup = BeautifulSoup(file, "lxml")
#     text_pieces = soup.find_all("p")
#
#     text_file = lol + xml.filename.replace(".xml", ".txt")
#     with open(text_file, "w") as handler:
#         for text in text_pieces:
#             handler.write(text.text)


with open(data_dir, "r") as file:
    sentences = tokenize.sent_tokenize(file.read())
    sentence_path = "data/1803-1820/S1V0001P0.csv"
    with open(sentence_path, "w+") as sentences_file:
        writer = csv.writer(sentences_file, delimiter= "\n")
        writer.writerow(sentences)


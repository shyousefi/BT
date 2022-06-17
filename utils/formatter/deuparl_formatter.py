import os
import re

extracted_sentences = "/ukp-storage-1/krause/Thesis/data/DeuParl/extracted_sentences/with_dates"


def replace_hyphen(text):
    matches = re.findall("\S- ", text)
    for match in matches:
        text = text.replace(match, match[0])
    return text


for file in os.listdir(extracted_sentences):
    path = os.path.join(extracted_sentences, file)
    text = []
    with open(path, "r") as f:
        for line in f:
            tmp_line = line.replace("¬ ", "")
            tmp_line = replace_hyphen(tmp_line)
            text = text + [tmp_line]
        f.close()
    with open(path, "w") as f:
        f.writelines(text)
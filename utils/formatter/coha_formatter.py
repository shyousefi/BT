import os

coha_path = "/ukp-storage-1/krause/Thesis/data/COHA/extracted_sentences/with_dates"


for file in os.listdir(coha_path):
    text = ""
    txt_path = os.path.join(coha_path, file)
    with open(txt_path, "r") as reader:
        for line in reader:
            new_line = line.replace(" '", "'")
            new_line = new_line.replace(" // ", " ")
            new_line = new_line.replace(" n't", "n't")
            text = text + new_line
    with open(txt_path, "w") as writer:
        writer.write(text)
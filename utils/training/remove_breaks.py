from asyncore import write
import os

training_sets = "/ukp-storage-1/krause/Thesis/results/training_sets"

def remove_unnecessary_breaks(file_path):
    if (file_path.endswith(".conllu")):
        text = ""
        with open(file_path, "r") as reader:
            text = reader.read()
            text.replace("\n\n\n","\n\n")
        with open(file_path, "w") as writer:
            writer.write(text)
            return True
    return False


for folder in os.listdir(training_sets):
    folder_path = os.path.join(training_sets, folder)
    for file in os.listdir(folder_path):
        f_path = os.path.join(folder_path, file)
        removed = remove_unnecessary_breaks(f_path)       
        if not removed and os.path.isdir(file):
            for conllu in os.listdir(f_path):
                conllu_path = os.path.join(f_path, conllu)
                remove_unnecessary_breaks(conllu_path)

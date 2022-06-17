import re

txt = "/ukp-storage-1/krause/Thesis/results/extracted_sentences/Hansard.txt"

with open(txt, "r") as reader:
    text = reader.read()
    negatives = len(re.findall("\sn\n", text))
    positives = len(re.findall("\sy\n", text))
    unsure = len(re.findall("\sm\n", text))
    percentage = ((unsure / 2) + positives)
    print("Negatives: ", negatives)
    print("Positives: ", positives)
    print("Unsure: ", unsure)
    print("Percentage: ", percentage)
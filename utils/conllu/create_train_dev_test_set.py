import os
import random

ud_path = "/ukp-storage-1/krause/Thesis/data/ud/ud-treebanks-v2.9/UD_English-EWT"
result_path = "/ukp-storage-1/krause/Thesis/results/train_dev_test_set/english/EWT"
seed = 1337

random.seed(seed)


def extract_set(file_name, amount):
	file_path = os.path.join(ud_path, file_name)
	texts = []
	with open(file_path, "r") as reader:
		text = reader.read()
		texts = text.split("\n\n")

	random.shuffle(texts)
	out_path = os.path.join(result_path, file_name.split("-")[-1])
	with open(out_path, "a") as writer:
		while amount > 0 and texts:
			text = texts.pop()
			rows = text.split("\n")
			if len(rows) > 50 or len(rows) < 2:
				continue
			writer.write(text)
			writer.write("\n\n")


for file in os.listdir(ud_path):
	if not file.endswith(".conllu"):
		continue
	if file.__contains__("train"):
		extract_set(file, 1000)
	elif file.__contains__("dev") or file.__contains__("test"):
		extract_set(file, 300)
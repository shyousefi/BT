import os
from pathlib import Path
import random

gold_files = "/ukp-storage-1/krause/Thesis/data/gold"
result_dir = "/ukp-storage-1/krause/Thesis/results/trainning_sets/gold"
seed = 1337

random.seed(seed)
for conllu in os.listdir(gold_files):
	if conllu.endswith(".conllu"):
		conllu_path = os.path.join(gold_files, conllu)
		sentences = []
		with open(conllu_path, "r") as reader:
			text = reader.read()
			sentences = text.split("\n\n")
			reader.close()

		random.shuffle(sentences)
		#train dev test split 70/15/15
		result_path = os.path.join(result_dir, conllu.replace(".conllu", ""))
		Path(result_path).mkdir(exist_ok=True, parents=True)
		with open(os.path.join(result_path, "train.conllu"), "w") as writer:
			writer.write("\n\n".join(sentences[:int(len(sentences) * 0.7)]))

		with open(os.path.join(result_path, "dev.conllu"), "w") as writer:
			writer.write("\n\n".join(sentences[int(len(sentences) * 0.7):int(len(sentences) * 0.85)]))

		with open(os.path.join(result_path, "test.conllu"), "w") as writer:
			writer.write("\n\n".join(sentences[int(len(sentences) * 0.85):]))

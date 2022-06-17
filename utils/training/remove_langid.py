import os
from pathlib import Path

data_with_langids = "/ukp-storage-1/krause/Thesis/results/trainning_sets/eng"
result_dir = "/ukp-storage-1/krause/Thesis/results/trainning_sets/eng"

Path(result_dir).mkdir(parents=True, exist_ok=True)
for conllu in os.listdir(data_with_langids):
	conllu_path = os.path.join(data_with_langids, conllu)
	with open(conllu_path, "r") as reader:
		data = reader.read().replace("\ten\n", "\n")
		data = data.replace("\tde\n", "\n")
	result_conllu = os.path.join(result_dir, conllu)
	with open(result_conllu, "w") as writer:
		writer.write(data)
		writer.close()
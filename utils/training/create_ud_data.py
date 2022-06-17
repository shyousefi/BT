import os
from pathlib import Path

base_dir = "/ukp-storage-1/krause/Thesis/results/trainning_sets/"
unedited_data = os.path.join(base_dir, "gold")
lang_data = os.path.join(base_dir, "gold_udapter")

for directory in os.listdir(unedited_data):
	lan = "en" if directory == "27329" else "de"
	directory_path = os.path.join(unedited_data, directory)
	for conllu in os.listdir(directory_path):
		conllu_path = os.path.join(directory_path, conllu)
		text = ""
		with open(conllu_path, "r") as reader:
			for line in reader:
				if line[0] == "\n" or line[0] == "#":
					text = text + line
				else:
					new_line = line.replace("\n", "") + "\t" + lan + "\n"
				text = text + new_line
			reader.close()

		result_dir = os.path.join(lang_data, directory)
		Path(result_dir).mkdir(exist_ok=True, parents=True)
		result_conllu = os.path.join(result_dir, conllu)
		with open(result_conllu, "w") as writer:
			writer.write(text)
			writer.close()
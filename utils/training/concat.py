import os
from pathlib import Path

few_shot_data = "/ukp-storage-1/krause/Thesis/data/training_few_shot"
crfpar_data = {"de": "/ukp-storage-1/krause/Thesis/results/training_sets/ger/train.conllu", "en": "/ukp-storage-1/krause/Thesis/results/training_sets/eng/train.conllu"}
ud_data = "/ukp-storage-1/krause/Thesis/results/training_sets/ud/train.conllu"
ndmv_data = {"de": "/ukp-storage-1/krause/Thesis/results/training_sets/ger_gsd/train.conllu", "en": "/ukp-storage-1/krause/Thesis/results/training_sets/eng_ewt/train.conllu"}


def concat_ud(dir_path, data_path, got_ud):
	tmp_dir = "ud/tmp/train.conllu"
	tmp_path = os.path.join(dir_path, tmp_dir)
	if got_ud:
		res_dir = os.path.join("ud", "train.conllu")
		res_path = os.path.join(dir_path, res_dir)
		concat(data_path, tmp_path, res_path)
	else:
		concat(data_path, ud_data, tmp_path)	
	

def concat_crfpar(dir_path, data_path, lan_id):
	crfpar_path = crfpar_data[lan_id]
	res_directory = os.path.join("crfpar-" + lan_id, "train.conllu")
	res_path =os.path.join(dir_path, res_directory)
	concat(data_path, crfpar_path, res_path)


def concat_ndmv(dir_path, data_path, lan_id):
	ndmv_path = crfpar_data[lan_id]
	res_directory = os.path.join("ndmv-" + lan_id, "train.conllu")
	res_path =os.path.join(dir_path, res_directory)
	concat(data_path, ndmv_path, res_path)


def concat(concat_data_path, base_data_path, out_path):
	concat_data = ""
	with open(concat_data_path, "r") as reader:
		concat_data = reader.read()
		reader.close()
	base_data = ""
	with open(base_data_path, "r") as reader:
		base_data = reader.read()
		reader.close()
	data = base_data + concat_data
	Path("/".join(out_path.split("/")[:-1])).mkdir(parents=True, exist_ok=True)
	with open(out_path, "w") as writer:
		writer.write(data)
	pass


if __name__ == "__main__":
	for directory in os.listdir(few_shot_data):
		dir_path = os.path.join(few_shot_data, directory)
		if not os.path.isdir(dir_path):
			continue
		got_ud = False
		for conllu in os.listdir(dir_path):
			if not conllu.endswith(".conllu"):
				continue
			conllu_path = os.path.join(dir_path, conllu)
			if conllu_path.__contains__("ud"):
				concat_ud(dir_path, conllu_path, got_ud)
				got_ud = True
				continue
			lan_id = conllu.split(".")[0]
			concat_crfpar(dir_path, conllu_path, lan_id)
			concat_ndmv(dir_path, conllu_path, lan_id)


			
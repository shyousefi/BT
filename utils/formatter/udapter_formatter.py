import os
from pathlib import Path

base_dir = "/ukp-storage-1/krause/Thesis/data/Hansard"
udapter_files = os.path.join(base_dir, "udapter")
read_files = os.path.join(base_dir, "extracted_sentences")
lang = "en"

Path(udapter_files).mkdir(parents=True, exist_ok=True)
text = ""
with open("/ukp-storage-1/krause/Thesis/data/Hansard/extracted_sentences/random/1803-1810.txt", "r") as reader:
	for line in reader:
		line = line.strip()
		line = line + "\t" + lang + "\n"
		text = text + line

with open(os.path.join(udapter_files, "1803-1810.txt"), "a") as writer:
	writer.write(text)


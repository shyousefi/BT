import os
import zipfile
import re

coha_dir = "/ukp-storage-1/krause/Thesis/data/COHA/COHA"
out_dir = "/ukp-storage-1/krause/Thesis/data/COHA/unzipped"

for zip_file in os.listdir(coha_dir):
    zip_file_path = os.path.join(coha_dir, zip_file)
    if zipfile.is_zipfile(zip_file_path) and zip_file.__contains__("text_"):
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            year = re.search("\d{4}", zip_file).group(0)
            result_dir = os.path.join(out_dir, year + "-" + year[:-1] + "9")
            zip_ref.extractall(result_dir)
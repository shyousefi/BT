import os
import re
import zipfile

hansard_path = "/ukp-storage-1/krause/Thesis/data/Hansard"
for file in os.listdir(hansard_path):
    zip_path = os.path.join(hansard_path, file)
    for zip_file in os.listdir(zip_path):
        zip_file_path = os.path.join(zip_path, zip_file)
        if zip_file_path.endswith(".txt"):
            os.remove(zip_file_path)
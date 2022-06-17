import pandas as pd
import os

csv_path = "/ukp-storage-1/krause/Thesis/data/Hansard/csv"

for directory in os.listdir(csv_path):
    path = os.path.join(csv_path, directory)
    li = []
    for csv in os.listdir(path):
        file = os.path.join(path, csv)
        if file.endswith(".csv"):
            print(file)
            df = pd.read_csv(file, header=0, sep="\t", delimiter="\t")
            li.append(df)
            os.remove(file)

    frame = pd.concat(li, axis=0, ignore_index=True)
    frame.to_csv(os.path.join(path, directory + ".csv"), sep="\t", header=["debates", "date", "title"])
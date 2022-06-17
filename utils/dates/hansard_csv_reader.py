import os
import pandas as pd

hansard_csv = "/ukp-storage-1/krause/Thesis/data/Hansard/csv"

def read():
    hansard = pd.DataFrame(columns=["debates", "date"])
    for csv in os.listdir(hansard_csv):
        csv_path = os.path.join(hansard_csv, csv)
        content = pd.read_csv(csv_path, sep="\t", usecols=["debates", "date"])
        hansard = pd.concat([hansard, content])
    return hansard
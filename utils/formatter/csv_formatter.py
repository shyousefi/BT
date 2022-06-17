import os
import pandas as pd

hansard_excerpt_path = "/ukp-storage-1/krause/Thesis/data/Hansard/hansard-speeches-v301.csv"
csv_path = "/ukp-storage-1/krause/Thesis/data/Hansard/csv"

df = pd.read_csv(hansard_excerpt_path, usecols=["speech", "date"])



import csv
import os.path

import pandas as pd

hansard_path = "/ukp-storage-1/krause/Thesis/data/Hansard/hansard-speeches-v301.csv"
csv_path = "/ukp-storage-1/krause/Thesis/data/Hansard/csv"

DEBATES = "debates"
DATE = "date"
YEAR = "year"
SPEECH = "speech"
TITLE = "title"
HEADING = "major_heading"

with open(hansard_path, "r") as csv_file:
    reader = csv.DictReader(csv_file, delimiter=",", quotechar='"')
    previous_year = 1979
    count = 0
    for line in reader:
        date = line[DATE]
        year = previous_year
        if date:
            year = int(date.split("-")[0])
            previous_year = year
        if year < 1980:
            continue
        df = pd.DataFrame({DEBATES: line[SPEECH], DATE: date, TITLE: line[HEADING]}, index=[0])
        last_digit = year % 10
        beginning_year = year - last_digit + 1 if last_digit > 0 else year - 9
        name = str(beginning_year) + "-" + str(beginning_year + 9)
        csv_dir = os.path.join(csv_path, name + ".csv")
        if not os.path.isfile(csv_dir):
            df.to_csv(csv_dir, mode='w', header=True, index=False, sep="\t")
        df.to_csv(csv_dir, mode='a', header=False, index=False, sep="\t")
        count += 1
    print(count)
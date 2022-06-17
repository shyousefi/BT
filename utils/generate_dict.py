import json
file = "/ukp-storage-1/krause/Thesis/utils/test.txt"
letter_codes = "/ukp-storage-1/krause/Thesis/parsers/udapter/languages/letter_codes.json"

json1_file = open(letter_codes)
json1_str = json1_file.read()
json1_data = json.loads(json1_str)


with open(file, "r") as reader:
    dictionary = {}
    for line in reader:
        line = line.replace("\n", "")
        if line in json1_data:
            continue
        dictionary[line] = line
    print(dictionary)

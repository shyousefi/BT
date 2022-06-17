from subprocess import check_output
import json
import re
from bs4 import BeautifulSoup

distinct_sentences = "/ukp-storage-1/krause/Thesis/utils/dates/de_distinct.json"
bash_script = "./grep.sh"
bund = "/ukp-storage-1/krause/Thesis/data/Bundestagsprotokolle"
reich = "/storage/nllg/compute-share/bodensohn/deuparl/DeuParl/data/5_postprocessed/Reichstag"
hansard = "/ukp-storage-1/krause/Thesis/data/Hansard/csv"


def grep(tmp, entry):
    try: 
        out = check_output(["grep", "-i", "-R", "-I", tmp, bund]).decode()[:-1]
        return write_out(out, entry)
    except:
        print("Error")
    try:
        out = check_output(["grep", "-i", "-R", "-I", tmp, reich]).decode()[:-1]
        return write_out(out, entry)
    except:
        return False
    try:
        out = check_output(["grep", "-i", "-R", "-I", tmp, hansard]).decode()[:-1]
        return write_out(out, entry)
    except:
        return False


def write_out(out, entry):
    lines = out.split("\n")
    match = re.search("/(1\d{3})/", out)
    if len(lines) == 1 and match:
        date = match.group(1)
        with open("certain.txt", "a") as writer:
            writer.write(entry +"\t" + date)
            writer.write("\n")
            writer.write(out)
            writer.write("\n")
            return True
    elif (len(lines) == 2 and not match):
        file = out.split(":")[1]
        f = open(file).read()
        soup = BeautifulSoup(f)
        date = soup.find_all("Datum")[0]
        with open("certain.txt", "a") as writer:
            writer.write(entry + "\t" +date)
            writer.write("\n")
            writer.write(out)
            writer.write("\n")
            return True
    elif (len(lines)) == 1 and hansard in out:
        with open("han_certain.txt", "a") as writer:
            date = lines[0].split("\t")[1]
            writer.write(entry +"\t" + date)
            writer.write("\n")
            writer.write(out)
            writer.write("\n")
            return True
    else:
        return False
    

def main():
    with open(distinct_sentences, "r") as f:
        data = json.load(f)
    for entry in data:
        words = entry.split(" ")
        tmp = entry
        certain = False
        for i in range(len(words)-1):
            tmp = tmp.replace(words[i] + " ", "")
            certain = grep(tmp, entry)
            if certain:
                break
        if certain:
            continue
        tmp = entry
        for i in range(len(words)-1):
            tmp = tmp.replace(" " + words[-i -1], "")
            certain = grep(tmp, entry)
            if certain:
                break
        if certain:
            continue
        with open("uncertain.txt", "a") as writer:
            writer.write(entry)
            writer.write("\n")
                

if __name__ == "__main__":
    main()
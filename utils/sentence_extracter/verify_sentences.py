import os
from pathlib import Path
from tkinter import Y

path = "/ukp-storage-1/krause/Thesis/results/extracted_sentences"
eval_path = "/ukp-storage-1/krause/Thesis/results/extracted_sentences/eval"


def write_results(correct, incorrect, unclear, out_path):
    with open(out_path, "w") as writer:
                total = correct + incorrect + unclear
                if total == 0:
                    return
                writer.write("Correct: " + str(correct) + "\n")
                writer.write("Incorrect: " + str(incorrect) + "\n")
                writer.write("Unclear: " + str(unclear) + "\n")
                correct_percentage = ((unclear/2) + correct) / total
                writer.write("Percentage: " + str(correct_percentage))


for directory in os.listdir(path):
    if directory == "eval":
        continue
    dir_path = os.path.join(path, directory)
    y_all = 0
    n_all = 0
    m_all = 0
    if os.path.isdir(dir_path):
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            y = 0
            n = 0
            m = 0
            with open(file_path, "r") as reader:
                for line in reader:
                    if len(line) < 2:
                        print("Error in file: " + file_path)
                        print(line)
                        continue
                    if line[-2] == "y":
                        y += 1
                    elif line[-2] == "n":
                        n += 1
                    elif line[-2] == "m":
                        m += 1
                    else:
                        pass
                        #print("Error in file: " + file_path)
                        #print(line)
            y_all += y
            n_all += n
            m_all += m
            eval = os.path.join(eval_path, directory)
            Path(eval).mkdir(parents=True, exist_ok=True)
            result_path = os.path.join(eval, file.replace(".txt", "_eval.txt"))
            write_results(y, n, m, result_path)
        all_results = os.path.join(eval_path, directory + "_eval.txt")
        write_results(y_all, n_all, m_all, all_results)
        
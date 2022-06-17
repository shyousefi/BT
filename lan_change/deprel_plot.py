import matplotlib.pyplot as plt
import os
import numpy as np


paths = ["/ukp-storage-1/krause/Thesis/results/towerparse/COHA", "/ukp-storage-1/krause/Thesis/results/towerparse/DeuParl", "/ukp-storage-1/krause/Thesis/results/towerparse/Hansard"]

def choose_pattern(tag):
    if "incr" in tag:
        return "b", "-"
    elif "decr" in tag:
        return  "grey", "/" 
    else:
        return "w", ""

def main():
    for path in paths:
        for file in os.listdir(path):
            if "_maj_" not in file and "_min_" not in file:
                continue
            if not file.endswith(".table"):
                continue
            file_path = os.path.join(path, file)
            
            averages = np.array([])
            labels = np.array([])
            tags = np.array([])
            p_values = np.array([])
            occurrences = np.array([])
            with open(file_path, "r") as reader:
                for line in reader:
                    tmp = line.replace("\\\\\n", "")
                    line_data = tmp.split(" & ")
                    if len(line_data) != 5:
                        continue
                    averages = np.append(averages, float(line_data[3]))
                    labels = np.append(labels, line_data[0])
                    p_values = np.append(p_values, float(line_data[2]))
                    tags = np.append(tags, line_data[1])
                    occurrences = np.append(occurrences, line_data[4])

            colors = np.array([])
            patterns = np.array([])
            for tag in tags:
                color, pat = choose_pattern(tag)
                colors = np.append(colors, color)
                patterns = np.append(patterns, pat)
            

            fig, ax = plt.subplots()
            sorted_indeces = averages.argsort()

            colors
            ax.bar(x=np.arange(len(sorted_indeces)), height=averages[sorted_indeces], color=colors[sorted_indeces], hatch=patterns[sorted_indeces], tick_label=labels[sorted_indeces], edgecolor="k")
            plt.xticks(rotation=70)

            final = file_path.replace(".table", ".png")
            fig.savefig(final)
            print("averages")
            
            fig2, ax2 = plt.subplots()
            sorted_indeces = occurrences.argsort()
            ax2.bar(x=np.arange(len(sorted_indeces)), height=occurrences[sorted_indeces], tick_label=labels[sorted_indeces], edgecolor="k")
            plt.xticks(rotation=70)
            fig2.savefig(final.replace("/mk_", "/occ_mk_"))



if __name__ == "__main__":
    main()
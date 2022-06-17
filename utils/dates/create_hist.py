import matplotlib.pyplot as plt
import numpy as np
import re

hansard = "hansard.txt"
deuparl = "deuparl.txt"


def draw(path, file):
    years = []    
    with open(path, "r") as reader:
        for line in reader:
            match = re.search("(\d{4})-", line)
            if match:
                year = match.group(1)
                years += [year]
                continue
            match = re.search("\.(\d{4})", line)
            if match:
                year = match.group(1)
                years += [year]
                continue
            match = re.search("(\d{4})\n", line)
            if match:
                year = match.group(1)
                years += [year]
                continue
            print("NO Match for: " + line)
    
    years_set = set(years)
    years = sorted(years)
    print(years)
    fig, ax = plt.subplots(1,1)
    ax.hist(years, bins=np.arange(len(years_set)) -0.4, width=0.8)
    fig.gca().margins(x=0)
    plt.gcf().canvas.draw()
    tl = fig.gca().get_xticklabels()
    maxsize = max([t.get_window_extent().width for t in tl])
    m = 0.2 # inch margin
    s = maxsize/plt.gcf().dpi*len(years)+2*m
    margin = m/plt.gcf().get_size_inches()[0]

    plt.gcf().subplots_adjust(left=margin, right=1.-margin)
    plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])
    ax.set_xlabel('Years')
    ax.set_ylabel('Count')
    ax.tick_params(axis='x', labelsize=20)

    fig.savefig(file)
    

def main():
    draw(hansard, "hansard.png")
    draw(deuparl, "deuparl.png")


if __name__ == "__main__":
    main()
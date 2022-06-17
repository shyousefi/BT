import matplotlib.pyplot as plt
import os
import json

import numpy as np
import itertools

results_dir = "/ukp-storage-1/krause/Thesis/results/udapter"
corpora = ["Hansard", "DeuParl", "COHA"]


def create_lines_distinction():
    linestyles = [(0, ()), (0, (1, 10)), (0, (1, 1)), (0, (5, 10)), (0, (5, 5)), (0, (3, 5, 1, 5))]
    markers = ["o", "^", "s", "P", "D"]

    return list(itertools.product(linestyles,markers))


def deuparl_period(period):
    deu_map = {1: 1890, 2: 1918, 3: 1933, 4: 1942, 5: 1969, 6: 1982, 7: 1998, 8: 2005, 9: 2020}
    return deu_map[period]

def get_out_base(path):
    folder = path.split("/")
    if "tower" in path:
        return folder[-2] + "_" + folder[-1] + "_"
    return folder[-3] + "_" + folder[-2] + "_"


def make_graphs(path):
    for directory in os.listdir(path):
        print(path)
        if directory == "eval":
            continue
        corpus_dir = os.path.join(path, directory)

        periods = np.array([])
        res_length= np.array([])
        res_norm_dlm = np.array([])
        res_root_dist= np.array([])
        res_max_degree= np.array([])
        res_norm_height= np.array([])
        res_in_deg_var = np.array([])
        res_normed_cross = np.array([])
        json_files = sorted(os.listdir(corpus_dir))
        for json_file in json_files:
            if not json_file.endswith(".json"):
                continue
            json_dir = os.path.join(corpus_dir, json_file)
            with open(json_dir, "r") as f:
                json_data = json.load(f)
            data = json_data["data"]

            date = [x["date"] for x in data]
            length = np.array([x["length"] for x in data])
            mean_dlm = [x["mean_dlm"] for x in data]
            norm_dlm = np.array([x["norm_dlm"] for x in data])
            root_dist = np.array([x["root_dist"] for x in data])
            max_degree = np.array([x["max_degree"] for x in data])
            largest_sing_dist = [x["largest_sing_dist"] for x in data]
            root_height = [x["root_height"] for x in data]
            norm_height = np.array([x["norm_height"] for x in data])
            max_dn_height = [x["max_dn_height"] for x in data]
            in_degree_var = np.array([x["in_degree_var"] for x in data])
            norm_cross = np.array([x["normed_cross"] for x in data])

            hist_fig, hist_ax = plt.subplots()
            hist_ax.hist(norm_dlm)
            hist_ax.set_xlabel("Norm. DL")
            hist_png = os.path.join(corpus_dir, "height_"+ json_file.replace(".json", ".png"))
            hist_fig.savefig(hist_png)

            period = 0
            if "DeuParl" in corpus_dir:
                period = deuparl_period(int(json_file.split("-")[0]))
            else:
                period = int(json_file.split("-")[1].replace(".json", ""))
            periods= np.append(periods, period)

            res_length = np.append(res_length, length.mean())
            res_norm_dlm = np.append(res_norm_dlm, norm_dlm.mean())
            res_max_degree = np.append(res_max_degree, max_degree.mean())
            res_root_dist = np.append(res_root_dist, root_dist.mean())
            res_norm_height = np.append(res_norm_height, norm_height.mean())
            res_in_deg_var = np.append(res_in_deg_var, in_degree_var.mean())
            res_normed_cross = np.append(res_normed_cross, norm_cross.mean())
        if periods.size == 0:
            continue
            
        corpus = ""
        for c in corpora:
            if c in path:
                corpus = c
                break
        print(corpus_dir)
        
        outbase = get_out_base(corpus_dir)
        coef = np.polyfit(periods,res_norm_dlm,deg=1)
        poly1d_fn = np.poly1d(coef)
        norm_fig, norm_ax = plt.subplots()
        norm_ax.plot(periods, res_norm_dlm, "bo", periods, poly1d_fn(periods), '--k')
        norm_ax.set_xlabel("Year")
        norm_ax.set_ylabel("Normalized DL")
        ndlm_png = os.path.join(corpus_dir, outbase + "ndlm_"+ corpus + ".png")
        norm_fig.savefig(ndlm_png)

        coef = np.polyfit(periods,res_length,deg=1)
        poly1d_fn = np.poly1d(coef)
        length_fig, length_ax = plt.subplots()
        length_ax.plot(periods, res_length, "bo", periods, poly1d_fn(periods), '--k')
        length_ax.set_xlabel("Year")
        length_ax.set_ylabel("Sentence Length")
        length_png = os.path.join(corpus_dir, outbase + "length_"+ corpus + ".png")
        length_fig.savefig(length_png)

        coef = np.polyfit(periods,res_max_degree,deg=1)
        poly1d_fn = np.poly1d(coef)
        md_fig, md_ax = plt.subplots()
        md_ax.plot(periods, res_max_degree, "bo", periods, poly1d_fn(periods), '--k')
        md_ax.set_xlabel("Year")
        md_ax.set_ylabel("Max In-Degree")
        md_png = os.path.join(corpus_dir, outbase + "md_"+ corpus + ".png")
        md_fig.savefig(md_png)

        coef = np.polyfit(periods,res_norm_height,deg=1)
        poly1d_fn = np.poly1d(coef)
        nrh_fig, nrh_ax = plt.subplots()
        nrh_ax.plot(periods, res_norm_height, "bo", periods, poly1d_fn(periods), '--k')
        nrh_ax.set_xlabel("Year")
        nrh_ax.set_ylabel("Norm. Tree Height")
        nrh_png = os.path.join(corpus_dir, outbase + "height_"+ corpus + ".png")
        nrh_fig.savefig(nrh_png)

        coef = np.polyfit(periods,res_in_deg_var,deg=1)
        poly1d_fn = np.poly1d(coef)
        idv_fig, idv_ax = plt.subplots()
        idv_ax.plot(periods, res_in_deg_var, "bo", periods, poly1d_fn(periods), '--k')
        idv_ax.set_xlabel("Year")
        idv_ax.set_ylabel("In-degree Variance")
        idv_png = os.path.join(corpus_dir, outbase + "idv_"+ corpus + ".png")
        idv_fig.savefig(idv_png)
        
        coef = np.polyfit(periods,res_normed_cross,deg=1)
        poly1d_fn = np.poly1d(coef)
        idv_fig, idv_ax = plt.subplots()
        idv_ax.plot(periods, res_normed_cross, "bo", periods, poly1d_fn(periods), '--k')
        idv_ax.set_xlabel("Year")
        idv_ax.set_ylabel("Normed Edge Crossings")
        idv_png = os.path.join(corpus_dir, outbase + "nec_"+ corpus + ".png")
        idv_fig.savefig(idv_png)


        sorted_lengths, sorted_norms = zip(*sorted(zip(res_length, res_norm_dlm)))
        coef = np.polyfit(sorted_lengths, sorted_norms,deg=1)
        poly1d_fn = np.poly1d(coef)
        sl_fig, sl_ax = plt.subplots()
        sl_ax.plot(sorted_lengths, sorted_norms, "bo", sorted_lengths, poly1d_fn(sorted_lengths), '--k')
        sl_ax.set_xlabel("Sentence Length")
        sl_ax.set_ylabel("Normalized DL")
        sl_png = os.path.join(corpus_dir,  outbase + "sl_"+ corpus + ".png")
        sl_fig.savefig(sl_png)







def main():
    if "towerparse" in results_dir:
        make_graphs(results_dir)
    else:
        for directroy in os.listdir(results_dir):
            if not any(directroy == x for x in corpora):
                continue
            path = os.path.join(results_dir, directroy)
            make_graphs(path)


if __name__ == "__main__":
    main()
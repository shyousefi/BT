import pymannkendall as mk
import os
import json
import numpy as np


paths = ["/ukp-storage-1/krause/Thesis/results/towerparse/COHA", "/ukp-storage-1/krause/Thesis/results/towerparse/DeuParl", "/ukp-storage-1/krause/Thesis/results/towerparse/Hansard"]

#"/ukp-storage-1/krause/Thesis/results/udapter/Hansard/few_shot", "/ukp-storage-1/krause/Thesis/results/udapter/DeuParl/few_shot", "/ukp-storage-1/krause/Thesis/results/udapter/COHA/few_shot"
#"/ukp-storage-1/krause/Thesis/results/udapter/COHA/modern", "/ukp-storage-1/krause/Thesis/results/udapter/DeuParl/modern", "/ukp-storage-1/krause/Thesis/results/udapter/Hansard/modern"
#"/ukp-storage-1/krause/Thesis/results/crfpar/DeuParl/modern", "/ukp-storage-1/krause/Thesis/results/crfpar/COHA/modern", "/ukp-storage-1/krause/Thesis/results/crfpar/Hansard/modern"
#"/ukp-storage-1/krause/Thesis/results/towerparse/COHA", "/ukp-storage-1/krause/Thesis/results/towerparse/DeuParl", "/ukp-storage-1/krause/Thesis/results/towerparse/Hansard"
corpora = ["DeuParl", "Hansard", "COHA"]


def get_out_name(path):
    folder = path.split("/")
    base_name = "mk" + "_" + folder[-3] + "_" +folder[-2]
    for corpus in corpora:
        if corpus == folder[-1]:
            base_name = "mk" + "_" + folder[-2] + "_" +folder[-1]
            break
    return base_name


def get_bound(file):
    info = file.replace(".json", "").split("-")
    if len(info[0]) == 1:
        deu_map = {1: 1890, 2: 1918, 3: 1933, 4: 1942, 5: 1969, 6: 1982, 7: 1998, 8: 2005, 9: 2020}
        return deu_map[int(info[0])]
    else:
        return int(info[1])


def main():
    for path in paths:
        norm_height = np.array([])
        norm_dlm = np.array([])
        norm_degree = np.array([])
        normed_cross = np.array([])
        dates = np.array([])
        bulk_rels = np.array([])
        for json_file in os.listdir(path):
            if not json_file.endswith(".json"):
                continue
            json_path = os.path.join(path, json_file)
            with open(json_path, "r") as reader:
                content = json.load(reader)
            if not content:
                continue
            data = content["data"]
            bulk_rels = np.append(bulk_rels, np.array([x["dep_rels"] for x in data]))
            dates = np.append(dates, np.array([x["date"] for x in data]))
            norm_height = np.append(norm_height, np.array([x["norm_height"] for x in data]))
            norm_dlm = np.append(norm_dlm, np.array([x["norm_dlm"] for x in data]))
            norm_degree = np.append(norm_degree, np.array([x["in_degree_var"] for x in data]))
            normed_cross = np.append(normed_cross, np.array([x["normed_cross"] for x in data]))
        sorted_indeces = dates.argsort()
        

        dep_rels = {}
        upper_bounds = sorted(list(filter(lambda x: x.endswith(".json"), os.listdir(path))))
        bound = get_bound(upper_bounds.pop(0))
        prop = {}
        print(upper_bounds)
        for i in sorted_indeces:
            date = dates[i]
            tmp_rels = bulk_rels[i]
            for key in tmp_rels:
                if key in dep_rels:
                    dep_rels[key]["dlm"] = np.append(dep_rels[key]["dlm"], tmp_rels[key]["dlm"])
                    dep_rels[key]["degree"] = np.append(dep_rels[key]["degree"], tmp_rels[key]["degree"])
                    dep_rels[key]["height"] = np.append(dep_rels[key]["height"], tmp_rels[key]["height"])
                    prop[key] += len(tmp_rels[key]["dlm"])
                else:
                    dep_rels[key] = {"dlm": np.array(tmp_rels[key]["dlm"]), "degree": np.array(tmp_rels[key]["degree"]), "height": np.array(tmp_rels[key]["height"])}
                    prop[key] = len(tmp_rels[key]["dlm"])
        

        prop_total = 0
        for key in prop.keys():
            prop_total += prop[key]

        out_file = get_out_name(path)
        major_dlm = out_file + "_deprel_maj_dlm.table"
        major_height = out_file + "_deprel_maj_height.table"
        major_degree = out_file + "_deprel_maj_degree.table"
        major_dlm = os.path.join(path, major_dlm)
        major_height = os.path.join(path, major_height)
        major_degree = os.path.join(path, major_degree)
        try: 
            os.remove(major_dlm)
        except:
            pass
        try:
            os.remove(major_height)
        except:
            pass
        try:
            os.remove(major_degree)
        except:
            pass
        print(out_file)
        for key in dep_rels.keys():
            print(key)
            if len(dep_rels[key]["dlm"]) != len(dep_rels[key]["degree"]) != len(dep_rels[key]["height"]) :
                print("Error")
                continue
            if len(dep_rels[key]["dlm"]) < 4:
                not_enough = out_file + "_deprel_ne.txt"
                not_enough = os.path.join(path, not_enough)
                with open(not_enough, "a") as writer:
                    writer.write(key + "\n")
                continue
            key_val_mk = mk.original_test(dep_rels[key]["dlm"])
            key_degree_mk = mk.original_test(dep_rels[key]["degree"])
            key_height_mk = mk.original_test(dep_rels[key]["degree"])
            if prop[key] <= prop_total*0.01:
                minor_dlm = out_file + "_deprel_min_dlm.table"
                minor_height = out_file + "_deprel_min_height.table"
                minor_degree = out_file + "_deprel_min_degree.table"
                minor_dlm = os.path.join(path, minor_dlm)
                minor_degree = os.path.join(path, minor_degree)
                minor_height = os.path.join(path, minor_height)
                with open(minor_dlm, "a") as writer:
                    writer.write(key + " & " + key_val_mk.trend + " & " + str("%.2f" % key_val_mk.p) + " & " + str("%.2f" % dep_rels[key]["dlm"].mean()) + " & " + str(len(dep_rels[key]["dlm"])) + "\\\\\n")
                with open(minor_height, "a") as writer:
                    writer.write(key + " & " + key_height_mk.trend + " & " + str("%.2f" % key_height_mk.p) + " & " + str("%.2f" % dep_rels[key]["height"].mean()) + " & " + str(len(dep_rels[key]["height"])) + "\\\\\n")
                with open(minor_degree, "a") as writer:
                    writer.write(key + " & " + key_degree_mk.trend + " & " + str("%.2f" % key_degree_mk.p) + " & " + str("%.2f" % dep_rels[key]["degree"].mean()) + " & " + str(len(dep_rels[key]["degree"])) + "\\\\\n")
                continue

            with open(major_dlm, "a") as writer:
                writer.write(key + " & " + key_val_mk.trend + " & " + str("%.2f" % key_val_mk.p) + " & " + str( "%.2f" % dep_rels[key]["dlm"].mean()) + " & " + str(len(dep_rels[key]["dlm"])) + "\\\\\n")
            with open(major_height, "a") as writer:
                writer.write(key + " & " + key_height_mk.trend + " & " + str("%.2f" % key_height_mk.p) + " & " + str("%.2f" % dep_rels[key]["height"].mean()) + " & " + str(len(dep_rels[key]["height"])) + "\\\\\n")
            with open(major_degree, "a") as writer:
                writer.write(key + " & " + key_degree_mk.trend + " & " + str("%.2f" % key_degree_mk.p) + " & " + str("%.2f" % dep_rels[key]["degree"].mean()) + " & " + str(len(dep_rels[key]["degree"])) + "\\\\\n")
        
        kandell = mk.original_test(norm_dlm[sorted_indeces])
        var_deg = mk.original_test(norm_degree[sorted_indeces])
        h = mk.original_test(norm_height[sorted_indeces])
        cross = mk.original_test(normed_cross[sorted_indeces])
        
        dlm_out = out_file + "_dlm.table"
        height_out = out_file + "_height.table"
        degree_out = out_file + "_degree.table"
        cross_out = out_file + "_cross.table"
        dlm_out = os.path.join(path, dlm_out)
        height_out = os.path.join(path, height_out)
        degree_out = os.path.join(path, degree_out)
        cross_out = os.path.join(path, cross_out)
        with open(dlm_out, "w") as writer:
            writer.write(kandell.trend + " & " + str("%.2f" % kandell.p) + "\\\\\n")
        with open(height_out, "w") as writer:
            writer.write(h.trend + " & " + str("%.2f" % h.p) + "\\\\\n")
        with open(degree_out, "w") as writer:
            writer.write(var_deg.trend + " & " + str("%.2f" % var_deg.p) + "\\\\\n")
        with open(cross_out, "w") as writer:
            writer.write(cross.trend + " &  " + str("%.2f" % var_deg.p)  + "\\\\\n")

        print("DLM")
        print(kandell)
        print("Degree")
        print(var_deg)
        print("Height")
        print(h) 


if __name__ == "__main__":
    main()
import os
import random
import re

gold_path = "/ukp-storage-1/krause/Thesis/data/gold"
out_path = "/ukp-storage-1/krause/Thesis/data/training_few_shot"

for conllu in os.listdir(gold_path):
    if conllu.__contains__(".conllu"):
        conllu_path = os.path.join(gold_path, conllu)
        lan_code = conllu.split(".")[0]
        sentences = []
        ud_sentences = []
        with open(conllu_path, "r") as reader:
            text = ""
            ud_text = ""
            for line in reader:
                text = text + line
                new_line = line
                if re.match("\d+\t", line):
                    new_line = line.replace("\n", "\t" + lan_code + "\n")
                ud_text = ud_text + new_line
            sentences = text.split("\n\n")
            ud_sentences = ud_text.split("\n\n")
            reader.close()
        random.shuffle(sentences)
        batch_count = 11
        batch_size = 0
        for i in range(3):
            batch_size += batch_count
            out_base = os.path.join(out_path, str(batch_size))
            conllu_out_path = os.path.join(out_base, conllu)
            conllu_ud_path = os.path.join(out_base, "ud-" + conllu)
            with open(conllu_out_path, "w") as writer:
                writer.write("\n\n".join(sentences[:batch_size]))
                writer.close()
            with open(conllu_ud_path, "w") as writer:
                writer.write("\n\n".join(ud_sentences[:batch_size]))
                writer.close()
        test_path = os.path.join(out_path, "test-" + conllu)
        with open(test_path, "w") as writer:
            writer.write("\n\n".join(sentences[batch_size:]))
        test_ud_path = os.path.join(out_path, "test-ud-" + conllu)
        with open(test_ud_path, "w") as writer:
            writer.write("\n\n".join(ud_sentences[batch_size:]))
            

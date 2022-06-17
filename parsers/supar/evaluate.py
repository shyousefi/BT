from cgi import test
from socket import TIPC_DEST_DROPPABLE
from supar import Parser
import os

model_path = "/ukp-storage-1/krause/Thesis/parsers/supar/model/eng_new.txt"
test_data = "/ukp-storage-1/krause/Thesis/data/training_few_shot/test-en.conllu"
result_path = "/ukp-storage-1/krause/Thesis/results/crfpar/eval/en_modern.txt"


loss, metric = Parser.load(model_path).evaluate(test_data, verbose=False)

with open(result_path, "w") as writer:
	writer.write("Loss: " + str(loss))
	writer.write("\n")
	writer.write(str(metric))
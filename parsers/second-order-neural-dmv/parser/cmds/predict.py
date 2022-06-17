# -*- coding: utf-8 -*-

from parser.cmds.cmd import CMD
from parser.helper.util import *
from parser.helper.loader_wrapper import LoaderWrapper
from parser.helper.data_module import DataModule
import torch


class Predict(CMD):

    def add_subparser(self, name, parser):
        subparser = parser.add_parser(
            name, help='Use a trained model to make predictions.'
        )

        return subparser

    
    def load_model(self, models, args):
        model = models["model"]
        model.load_state_dict(torch.load(args.state_dir))
        model.eval() 
        return model

    
    def _predict(self, loader, arg, model, dmv, dataset):
        model.eval()
        size = 0
        for x, y in loader:
            size += 1
            rules = model(x)
            if arg.decode != 'viterbi':
                ret = dmv._decode(rules, x['seq_len'], viterbi=True)["predicted_arc"]
            elif arg.decode != 'mbr':
                ret = dmv._decode(rules, x['seq_len'], mbr=True)["predicted_arc"]
            else:
                raise NotImplementedError
            print(ret.size())
            exit()


    def __call__(self, args):
        args.mode = "train"
        self.args = args
        dataset = DataModule(args)
        models = get_model(args.model, dataset)
        self.model = self.load_model(models, args)
        self.dmv = models['dmv']

        data_loader = LoaderWrapper(dataset.test_dataloader, dataset.device)
        self._predict(data_loader, args.test, self.model, self.dmv, dataset)
# -*- coding: utf-8 -*-

from parser.cmds.cmd import CMD
import torch
from parser.helper.metric import Metric
from parser.helper.util import *
from parser.helper.loader_wrapper import LoaderWrapper
from parser.helper.data_module import DataModule
from parser.trainer import KM_initializer

class Evaluate(CMD):

    def add_subparser(self, name, parser):
        subparser = parser.add_parser(
            name, help='Train a model.'
        )

        return subparser


    def load_model(self, models, args):
        model = models["model"]
        model.load_state_dict(torch.load(args.state_dir))
        model.eval() 
        return model


    def __call__(self, args):
        args.mode = "train"
        self.args = args
        dataset = DataModule(args)
        models = get_model(args.model, dataset)
        self.model = self.load_model(models, args)
        self.dmv = models['dmv']
        
        data_loader = LoaderWrapper(dataset.test_dataloader, dataset.device)
        self.model.eval()
        test_metric = self.evaluate(data_loader)
        with open(args.res_dir, "w") as writer:
           writer.write(f"{'test:':6}  {test_metric}")


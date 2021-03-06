import torch

import utility
import data
import model
import loss
from option import args
from trainer_multi import Trainer
from trainer_finetune import TrainerFT

torch.manual_seed(args.seed)
checkpoint = utility.checkpoint(args)

if checkpoint.ok:
    loader = data.Data(args)
    model = model.Model(args, checkpoint)
    # from IPython import embed; embed(); exit()
    loss = loss.Loss(args, checkpoint) if not args.test_only else None
    if args.model.lower() == 'finetune':
        t = TrainerFT(args, loader, model, loss, checkpoint)
    else:
        t = Trainer(args, loader, model, loss, checkpoint)
    while not t.terminate():
        t.train()
        t.test()

    checkpoint.done()


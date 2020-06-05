# -*- coding: utf-8 -*-
"""
    boris.cli
    ~~~~~~~~~

    A simple command line tool to train a state-of-the-art
    self-supervised model on your image dataset.

"""

import fire

from boris.data import ImageCollateFunction
from boris.data import BorisDataset
from boris.embedding import SelfSupervisedEmbedding
from boris.loss import NTXentLoss
from boris.models import ResNetSimCLR

import torch

def train_cli(data: str, root: str, download: bool = True, from_folder: str = '',
    batch_size=768, learning_rate=1e-0, weight_decay=1e-5, dim=16, **train_args):
    """ Train a self-supervised model on the image dataset of your choice.

    Args:
        data: Name of the dataset (to download use cifar10 or cifar100)
        root: Directory where the dataset should be stored
        download: Whether to download the dataset
        from_folder: If specified, the dataset is loaded from the folder
        batch_size: Number of negative samples is 2*(batch_size - 1)
        learning_rate: Learning rate for stochastic gradient descent
        weight_decay: Used for regularization
        dim: Dimensionality of the embedding space
        **train_args: Arguments passed to the trainer, 
                      see (https://pytorch-lightning.readthedocs.io/en/latest/trainer.html)

    Returns:
        checkpoint: (str) Path to checkpoint of the best model during training

    """

    model = ResNetSimCLR(num_ftrs=dim)
    criterion = NTXentLoss()
    optimizer = torch.optim.SGD(model.parameters(),
        lr=learning_rate, weight_decay=weight_decay
    )

    dataset = BorisDataset(root,
        name=data, train=True, download=download,
        from_folder=from_folder
    )

    dataloader = torch.utils.data.DataLoader(dataset,
        batch_size=batch_size, shuffle=True,
        collate_fn=ImageCollateFunction(),
        num_workers=8, drop_last=True
    )

    if not 'gpus' in train_args:
        train_args['gpus'] = 1 if torch.cuda.is_available() else 0
    
    encoder = SelfSupervisedEmbedding(model, criterion, optimizer, dataloader)
    encoder = encoder.train(**train_args) 

    print('Best model is stored at: %s' % (encoder.checkpoint))
    return encoder.checkpoint

if __name__ == '__main__':
    fire.Fire(train_cli)
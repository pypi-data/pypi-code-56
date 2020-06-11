# -*- coding: utf-8 -*-
"""
    boris.cli
    ~~~~~~~~~

    A simple command line tool to embed your image dataset using 
    a pretrained state-of-the-art, self-supervised model.

"""


from boris.data import ImageCollateFunction
from boris.data import BorisDataset
from boris.embedding import SelfSupervisedEmbedding
from boris.loss import NTXentLoss
from boris.models import ResNetSimCLR

import torch
import torchvision

import pandas as pd
import os

import hydra


def _to_pandas(embeddings, labels, filenames):
    csv = pd.DataFrame.from_records(embeddings)
    csv.index = filenames
    csv["label"] = labels
    return csv


def _embed_cli(cfg):
    """ Use the trained self-supervised model to embed samples from your dataset.

    Args:
        cfg[data]: (str) Name of the dataset
        cfg[root]: (str) Directory where the dataset should be stored
        cfg[checkpoint]: (str) Path to the lightning checkpoint 
        cfg[download]: (bool) Whether to download the dataset
        cfg[from_folder]: (str) If specified, the dataset is loaded from the folder

    Returns:
        embeddings: (np.ndarray) A 16-dimensional embedding for each data sample
        labels: (np.ndarray) Data labels, 0 if there are no labels
        filenames: (List[str]) File name of each data sample

    """

    data = cfg['data']
    root = cfg['root']
    checkpoint = cfg['checkpoint']
    download = cfg['download']
    from_folder = cfg['from_folder']

    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

    model = ResNetSimCLR(**cfg['model']).to(device)
    criterion = NTXentLoss(**cfg['criterion'])

    optimizer = torch.optim.SGD(model.parameters(), **cfg['optimizer'])

    transform = torchvision.transforms.Compose([
        torchvision.transforms.Resize(cfg['collate']['input_size']),
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize(
            mean=[0.485, 0.456, 0.406], 
            std=[0.229, 0.224, 0.225])
    ])

    dataset = BorisDataset(root,
        name=data, train=True, download=download,
        from_folder=from_folder, transform=transform
    )
    
    dataloader = torch.utils.data.DataLoader(dataset, **cfg['loader'])

    encoder = SelfSupervisedEmbedding.load_from_checkpoint(
        checkpoint, model, criterion, optimizer, dataloader,
        map_location=device,
    )

    embeddings, labels, filenames = encoder.embed(dataloader, device=device)

    df = _to_pandas(embeddings, labels, filenames)
    path = os.path.join(os.getcwd(), 'embeddings.csv')
    df.to_csv(path)
    print('Embeddings are stored at %s' % (path))
    
    return embeddings, labels, filenames


@hydra.main(config_path='./config/embed/config.yaml', strict=False)
def embed_cli(cfg):
    """ Use the trained self-supervised model to embed samples from your dataset.

    Args:
        cfg[data]: (str) Name of the dataset
        cfg[root]: (str) Directory where the dataset should be stored
        cfg[checkpoint]: (str) Path to the lightning checkpoint 
        cfg[download]: (bool) Whether to download the dataset
        cfg[from_folder]: (str) If specified, the dataset is loaded from the folder

    Returns:
        embeddings: (np.ndarray) A 16-dimensional embedding for each data sample
        labels: (np.ndarray) Data labels, 0 if there are no labels
        filenames: (List[str]) File name of each data sample

    """

    return _embed_cli(cfg)
    

def entry():
    embed_cli()
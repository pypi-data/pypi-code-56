# -*- coding: utf-8 -*-
"""
    boris.cli
    ~~~~~~~~~

    A simple command line tool to embed your image dataset using 
    a pretrained state-of-the-art, self-supervised model.

"""

import fire

from boris.data import ImageCollateFunction
from boris.data import BorisDataset
from boris.embedding import SelfSupervisedEmbedding
from boris.loss import NTXentLoss
from boris.models import ResNetSimCLR

import torch
import torchvision

def embed_cli(data: str, root: str, checkpoint: str, download: bool = False, from_folder: str =''):
    """ Use the trained self-supervised model to embed samples from your dataset.

    Args:
        data: Name of the dataset (to download use cifar10 or cifar100)
        root: Directory where the dataset should be stored
        checkpoint: Path to the lightning checkpoint 
        download: Whether to download the dataset
        from_folder: If specified, the dataset is loaded from the folder

    Returns:
        embeddings: (np.ndarray) A 16-dimensional embedding for each data sample
        labels: (np.ndarray) Data labels, 0 if there are no labels
        filenames: (List[str]) File name of each data sample

    """

    model = ResNetSimCLR()
    criterion = NTXentLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-0, weight_decay=1e-5)

    transform = torchvision.transforms.Compose([
        torchvision.transforms.Resize(32),
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize(
            mean=[0.485, 0.456, 0.406], 
            std=[0.229, 0.224, 0.225])
    ])

    dataset = BorisDataset(root,
        name=data, train=True, download=download,
        from_folder=from_folder, transform=transform
    )
    
    dataloader = torch.utils.data.DataLoader(dataset,
        batch_size=128, shuffle=True,
        num_workers=8, drop_last=True
    )

    encoder = SelfSupervisedEmbedding.load_from_checkpoint(
        checkpoint, model, criterion, optimizer, dataloader
    )

    embeddings, labels, filenames = encoder.embed(dataloader)
    
    return embeddings, labels, filenames

if __name__ == '__main__':
    fire.Fire(embed_cli)
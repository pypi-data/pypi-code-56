""" Embeddings """

import numpy as np

import time
import torch
from tqdm import tqdm 

from prefetch_generator import BackgroundGenerator
from ._base import BaseEmbedding

class SelfSupervisedEmbedding(BaseEmbedding):
    """ Self-supervised embedding based on contrastive multiview coding.
        (https://arxiv.org/abs/1906.05849)

    """

    def __init__(self, model, criterion, optimizer, dataloader):
        """ Constructor

        Args:
            model: (torch.nn.Module) 
            criterion: (torch.nn.Module)
            optimizer: (torch.optim.Optimizer)
            dataloader: (torch.utils.data.DataLoader)

        """ 

        super(SelfSupervisedEmbedding, self).__init__(
            model, criterion, optimizer, dataloader
        )
        

    def embed(self, dataloader, caching=False, normalize=False, device=None):
        """ Embed data in vector space

        Args:
            dataloader: (torch.utils.data.DataLoader)
            caching: (bool) TODO
            normalize: (bool) Normalize embeddings to unit length

        """

        # TODO: Caching
        if caching:
            pass
            return None, None
        
        self.model.eval()
        embeddings, labels, fnames = None, None, []

        pbar = tqdm(BackgroundGenerator(dataloader, max_prefetch=3),
                    total=len(dataloader))
        start_time = time.time()

        with torch.no_grad():

            for (img, label, fname) in pbar:

                img = img.to(device)
                label = label.to(device)

                fnames += [*fname]

                batch_size = img.shape[0]
                prepare_time = time.time()

                emb = self.model.features(img)
                emb = emb.detach().reshape(batch_size, -1)

                embeddings = emb if embeddings is None else torch.cat((embeddings, emb), 0)
                labels = label if labels is None else torch.cat((labels, label), 0)
                process_time = time.time()

                pbar.set_description("Compute efficiency: {:.2f}".format(
                    process_time / (process_time + prepare_time)))
                start_time = time.time()

            embeddings = embeddings.cpu().numpy()
            labels = labels.cpu().numpy()

        return embeddings, labels, fnames
        

class VAEEmbedding(BaseEmbedding):
    """ Unsupervised embedding based on variational auto-encoders.

    """

    def embed(self, dataloader):
        """ TODO

        """
        raise NotImplementedError("This site is under construction...")
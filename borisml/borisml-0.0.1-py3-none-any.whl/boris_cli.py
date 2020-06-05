# -*- coding: utf-8 -*-
"""
    boris.cli
    ~~~~~~~~~

    A simple command line tool to embed your image dataset with 
    state-of-the-art technology.

"""

import fire
import boris

class Boris(object):
    """ TODO Description

    """

    def all(self, data: str, root: str, download: bool = True, from_folder: str = '', **train_args):
        """ Train a self-supervised model on the image dataset of your choice, embed your images
            in vector space, explore and filter your data based on informative embeddings.

        Args:
            data: Name of the dataset (to download use cifar10 or cifar100)
            root: Directory where the dataset should be stored
            download: Whether to download the dataset
            from_folder: If specified, the dataset is loaded from the folder
            **train_args: Arguments passed to the trainer, 
                        see (https://pytorch-lightning.readthedocs.io/en/latest/trainer.html)
            TODO more...

        Returns:
            TODO

        Raises:
            TODO

        """

        checkpoint = boris.train_cli(data, root,
            download=download, from_folder=from_folder,
            **train_args
        )

        embeddings, labels, filenames = boris.embed_cli(data, root,
            download=False, from_folder=from_folder,
            checkpoint=checkpoint
        )
        
        # TODO
        boris.upload_cli()

    def train(self, data: str, root: str, download: bool = True, from_folder: str = '', **train_args):
        """ Train a self-supervised model on the image dataset of your choice

        Args:
            See boris.train_cli for details.
       
        """

        checkpoint = boris.train_cli(data, root,
            download=download, from_folder=from_folder,
            **train_args
        )

    def embed(self, data: str, root: str, checkpoint: str, download: bool = False, from_folder: str =''):
        """ Embed your image dataset 

        Args:
            See boris.embed_cli for details.
        
        """

        embeddings, labels, filenames = boris.embed_cli(data, root,
            download=False, from_folder=from_folder,
            checkpoint=checkpoint
        )

    def upload(self, *args, **kwargs):
        """ Upload your embeddings to our platform.

        Args:
            See boris.upload_cli for details.

        """

        # TODO
        boris.upload_cli()

    
    
if __name__ == '__main__':
    fire.Fire(Boris)
    

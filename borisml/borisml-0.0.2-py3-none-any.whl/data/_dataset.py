""" BorisDataset """

import torch.utils.data as data

import torchvision
import torchvision.datasets as datasets

import os

class BorisDataset(data.Dataset):
    """ Provides a uniform data interface for the embedding models.
    
    """

    def __init__(self, root='', name='cifar10', train=True, download=True, transform=None, from_folder=''):
        """ Initialize dataset from torchvision or from folder

        Args:
            root: (str) Directory where dataset is stored
            name: (str) Name of the dataset (e.g. cifar10, cifar100)
            train: (bool) Use the training set
            download: (bool) Download the dataset
            transform: (torchvision.transforms.Compose) image transformations
            from_folder: (str) Path to directory holding the images to load.
        """

        super(BorisDataset, self).__init__()
        if from_folder and os.path.exists(from_folder):
            # load data from directory
            self.dataset = datasets.ImageFolder(from_folder, transform=transform)
        elif name.lower() == 'cifar10':
            # load cifar10
            self.dataset = datasets.CIFAR10(root, train=train, download=download, transform=transform)
        elif name.lower() == 'cifar100':
            # load cifar100
            self.dataset = datasets.CIFAR100(root, train=train, download=download, transform=transform)
        else:
            raise ValueError('The specified dataset or data folder does not exist (%s, %s)' % \
                (name, from_folder))

    def __getitem__(self, index):
        """ Get item at index. Supports torchvision.ImageFolder datasets and 
            all dataset which return the tuple (sample, target).

        Args:
         - index:   index of the queried item

        Returns:
         - sample:  sample at queried index
         - target:  class_index of target class, 0 if there is no target
         - fname:   filename of the sample, str(index) if there is no filename

        """

        if isinstance(self.dataset, datasets.ImageFolder):
            fname = os.path.basename(self.dataset.imgs[index][0])
            sample, target = self.dataset.__getitem__(index)
            return sample, target, fname
        else:
            fname = str(index)
            sample, target = self.dataset.__getitem__(index)
            return sample, target, fname

    def __len__(self):
        """ Length of the dataset
        """
        return len(self.dataset)

    def __add__(self, other):
        """ Add element to dataset
        """
        raise NotImplementedError()
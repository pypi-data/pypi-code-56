""" ResNet for Self-Supervised Learning """

import torch
import torch.nn as nn

import torchvision.models as models

class ResNetSimCLR(nn.Module):

    def __init__(self, version='resnet-18', num_ftrs=16, out_dim=128):
        """ Constructor

        Args:
            version: (str) ResNet version from resnet-{18, 34, 50, 101, 152}
            num_ftrs: (int) Embedding dimension
            out_dim: (int) Output dimension

        """
        super(ResNetSimCLR, self).__init__()

        if version == 'resnet-18':
            resnet = models.resnet18()
        elif version == 'resnet-34':
            resnet = models.resnet34()
        elif version == 'resnet-50':
            resnet = models.resnet50()
        elif version == 'resnet-101':
            resnet = models.resnet101()
        elif version == 'resnet-152':
            resnet = models.resnet152()
        else:
            raise ValueError('Illegal version: {}. \
                Try resnet-18, resnet-34, resnet-50, resnet-101, resnet-152.')

        self.features = nn.Sequential(
            nn.BatchNorm2d(3),
            *list(resnet.children())[:-1],
            nn.Conv2d(512, num_ftrs, 1),
            nn.AdaptiveAvgPool2d(1)
        )

        # projection MLP
        self.l1 = nn.Linear(num_ftrs, num_ftrs)
        self.l2 = nn.Linear(num_ftrs, out_dim)
        self.relu = nn.ReLU()

    def forward(self, x):
        h = self.features(x)
        h = h.squeeze()

        x = self.l1(h)
        x = self.relu(x)
        x = self.l2(x)
        return x
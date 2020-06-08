"""
GMLP.game
=========
"""
from __future__ import absolute_import

import os

import pygame
from pygame.locals import QUIT


class Setup:
    """
    ``WARNING THIS FEATURE IS IN DEVELOPMENT!``
    GMLP 0.2 Setup. With Setup there are a few keywords that go with Setup.
    \nTo print the keywords type ``print(Setup.keywords)`` and it will print the keywords.
    """
    keywords = ['height', 'width', 'bg', 'name', 'objects']
    def __init__(self, **settings):
        for i in settings:
            if 'name' in settings:
                self.name = settings["name"]
            else:
                self.name = 'Window'

            if 'bg' in settings:
                self.bg = settings['bg']
            else:
                self.bg = (0, 0, 0)
            
            if 'height' in settings:
                self.h = settings['height']
            else:
                self.h = 0
            
            if 'width' in settings:
                self.w = settings['width']
            else:
                self.w = 0

            if 'objects' in settings:
                self.objects = settings['objects']
            else:
                self.objects = None
        
    def View(self, **kwargs):
        
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((self.h, self.w))
        pygame.display.set_caption(self.name)
        
        self.closed = False
        while not self.closed:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.closed = True

            self.gameDisplay.fill(self.bg)
            for image in range(len(kwargs['images'])):
                self.img = pygame.image.load(kwargs['images'][image])
                # if 'size' in kwargs:
                #     self.size = kwargs['size']
                #     self.img = pygame.transform.scale(self.img, self.size)
                # else:
                #     self.size = None
                if 'x' in kwargs:
                    self.x = kwargs['x']
                if 'y' in kwargs:
                    self.y = kwargs['y']
                self.gameDisplay.blit(self.img, (self.x, self.y))
            
            pygame.display.update()
        pygame.quit()


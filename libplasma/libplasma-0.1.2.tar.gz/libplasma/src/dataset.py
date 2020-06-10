#!/usr/bin/env python3

from random import randint
from libplasma.src.utils import *
import cv2
import shutil
from xxhash import xxh32_hexdigest
from datetime import datetime

class Image:
    def __init__(self,path,label):
        self.path = path
        self.data = cv2.imread(self.path)
        self.label = label

    def change_label(self,label):
        split_path = self.path.split('/')
        length = len(split_path)
        file_name = split_path[-1]
        dataset_path = '/'.join(split_path[:length-2])
        label_path = os.path.join(dataset_path,label)
        if not os.path.exists(label_path):
            os.mkdir(label_path)
        new_file_path = os.path.join(label_path,file_name)
        shutil.move(self.path,new_file_path)
        self.label = label


class ImageSet:
    def __init__(self,file_list,label):
        self.paths = file_list
        self.label = label
        self.file_count = len(file_list)

    def fetch_all(self):
        images = []
        for path in self.paths:
            image = Image(path,self.label)
            images.append(image)
        return images

    def next(self):
        file_name = next(self.paths)
        image = Image(file_name,self.label)
        return image


class Dataset:
    def __init__(self,name, data_type, version=None):
        self.name = name
        self.version = version
        self.type = data_type

    def _get_path(self):
        plasma_path = get_plasma_directory()
        dataset_path = os.path.join(
            plasma_path,
            'datasets',
            self.name)
        return dataset_path

    def _get_versioned_path(self):
        plasma_path = get_plasma_directory()
        dataset_path = os.path.join(
            plasma_path,
            'datasets',
            self.name,
            self.version)
        return dataset_path

    def get_path(self):
        if not self.version:
            path = self._get_path()
        else:
            path = self._get_versioned_path()
        return path

    def exists(self):
        dataset_path = self.get_path()
        return os.path.exists(dataset_path)

    def create(self):
        plasma_path = get_plasma_directory()
        dataset_path = self._get_path()
        if not os.path.exists(dataset_path):
            os.mkdir(dataset_path)
        if self.version is not None:
            versioned_path = self._get_versioned_path()
            if not os.path.exists(versioned_path):
                os.mkdir(versioned_path)

    def add(self, data_point, identifier=None, label='unlabelled'):
        if self.type == 'image':
            if not identifier:
                timestamp = datetime.now().strftime("%H_%M_%a")
                hash_string = xxh32_hexdigest(str(randint(0, 99999)))
                identifier = hash_string+'_'+timestamp + '.jpg'
            label_path = os.path.join(self.get_path(),label)
            if not os.path.exists(label_path):
                os.mkdir(label_path)
            file_name = os.path.join(label_path,identifier)
            cv2.imwrite(file_name, data_point)
        else:
            raise NotImplementedError

    def get(self,label='unlabelled'):
        if self.type == 'image':
            dataset_path = self.get_path()
            label_path = os.path.join(dataset_path,label)
            files = [ label_path+'/'+file_name for file_name in os.listdir(label_path)]
            data_point = ImageSet(files,label)
        return data_point


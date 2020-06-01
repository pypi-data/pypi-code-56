import cv2
import numpy as np
from torch.utils.data import Dataset


class DemoLiverDataset(Dataset):
    """

    Args:
        images_fps (list):
        masks_fps (list):
        augmentation (albumentations.Compose):
        preprocessing (albumentations.Compose):
        classes (list):
    """

    CLASSES = ['unlabelled', 'liver']

    classes_dict = {'unlabelled': 0, 'liver': 255}

    def __init__(self, images_fps, masks_fps,
                 classes,
                 augmentation=None, preprocessing=None,
                 ):

        self.images_fps = images_fps
        self.masks_fps = masks_fps

        # convert str names to class valued on masks
        assert isinstance(classes, list)
        self.class_values = [self.classes_dict[cls.lower()] for cls in classes]

        # data augmentation and preprocessing数据增强和预处理
        self.augmentation = augmentation
        self.preprocessing = preprocessing

    def __len__(self):
        return len(self.images_fps)

    def __getitem__(self, index):
        _image = cv2.imread(str(self.images_fps[index]))
        _image = cv2.cvtColor(_image, cv2.COLOR_BGR2RGB)
        _mask = cv2.imread(str(self.masks_fps[index]), 0)  # orginal mask is single channel原始的mask图像就是单通道的

        # extract certain classes from mask (e.g. liver) 从mask中提取特定的类
        _masks = [(_mask == v) for v in self.class_values]
        _mask = np.stack(_masks, axis=-1).astype('float')  # covert int8 to float将原来的0-255区间转换为0-1区间

        # apply augmentations
        if self.augmentation:
            sample = self.augmentation(image=_image, mask=_mask)
            _image, _mask = sample['image'], sample['mask']

        # apply preprocessing
        if self.preprocessing:
            sample = self.preprocessing(image=_image, mask=_mask)
            _image, _mask = sample['image'], sample['mask']

        sample = {'image': _image, 'label': _mask}

        # return sample
        return _image, _mask  # 为了配合segmentation_models_pytorch使用

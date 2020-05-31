import pandas as pd
import torch as T
from .glob_image_dir import GlobImageDir


class CheXpert(GlobImageDir):
    """Load CheXpert Dataset, assuming you already have a copy on disk.
    This loads the images and labels under the "train" directory, and applies
    optional transforms.

    An example usage looks like this:

        >>> dset = CheXpert(
            img_transform=tvt.Compose([
                tvt.RandomCrop((512, 512)),
                tvt.ToTensor(),
            ]),
            getitem_transform=lambda x: (
                x['image'],
                CheXpert.format_labels(x),  # chexpert provided labels from mining the writeup
                ]),
            )
        )
    """
    @staticmethod
    def format_labels(self, labels_vec: pd.Series, labels='all', ret_type=T.tensor):
        """Helper method for converting the labels into desired form, to be
        used in getitem_transform.  By default, fetch all labels as Torch tensor.

        The 14 diagnostic classes of interest have values:
            Nan: no diagnostic marking available
            -1: diagnosis uncertain
            0: negative
            1: positive
        We re-assign Nan to -2.

        :dct: the dict received in getitem_transform.
        :labels: either "all" or "diagnostic" or a list of label names.
            ['Sex', 'Age', 'Frontal/Lateral', 'AP/PA', 'No Finding',
            'Enlarged Cardiomediastinum', 'Cardiomegaly', 'Lung Opacity', 'Lung
            Lesion', 'Edema', 'Consolidation', 'Pneumonia', 'Atelectasis',
            'Pneumothorax', 'Pleural Effusion', 'Pleural Other', 'Fracture',
            'Support Devices'].

            Frontal/Lateral:  Frontal = 1, Lateral = 2.
            AP/PA:  nan=-2, AP=1, PA=2, LL=3, RL=4
            Male/Female: Unknown= 1, Female=2, Male=3
        :ret_type: - np.array or torch.tensor  (pytorch tensor by default)

        :returns: np.array or torch.tensor of numeric label values
        """
        lab = T.tensor(x['labels'])
        lab[T.isnan(lab)] = -2
        return lab

    def __init__(self, dataset_dir="./data/CheXpert-v1.0/"
                 use_train_set=True,
                 img_transform=tvt.ToTensor(),
                 getitem_transform=lambda x: (
                    x['image'], x['labels'])):

        train_or_valid = {'train' if use_train_set else 'valid'}
        img_fp_glob = f"{dataset_dir}/{train_or_valid}/patient*/study*/*.jpg"
        label_fp = f"{dataset_dir}/{train_or_valid}.csv"
        self.labels_csv = pd.read_csv(label_fp).set_index('Path')

        super().__init__(img_fp_glob, img_transform)

        match = re.search(f'CheXpert-v1.0(-small)?/{train_or_valid}/patient',
                  self.labels_csv.index[0])
        if match is None:
            raise Exception((
                "The directory containing CheXpert data should"
                " have either of these names, spelled exactly like this:"
                " CheXpert-v1.0 or CheXpert-v1.0-small."
                " Please pass a correct `dataset_dir`"))
        idx_for_fp_to_csv_matching = match.start()


    def __getitem__(self, index, _getitem_transform=True):
        sample = super().__getitem__(index)
        sample['labels'] = self.labels_csv.loc[
            sample['fp'][idx_for_fp_to_csv_matching:]]
        if _getitem_transform and self.__getitem_transform is not None:
            return self.__getitem_transform(sample)
        else:
            return sample


if __name__ == "__main__":
    # ipython -im simplepytorch.datasets.rite
    dset = RITE()

    print('z = dset[0] ; print(img, av_mask = z)')
    z = dset[0]
    img = z[:3]
    av_mask = z[3]
    print(img.shape, av_mask.shape)

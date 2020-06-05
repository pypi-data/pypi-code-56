""" BaseEmbeddings """

import torch
import torch.nn as nn
import pytorch_lightning as pl
import pytorch_lightning.core.lightning as lightning

def _handle_weak_labels(weak_label_src, weak_labels, fnames, embeddings):
    """ DESCRIPTION

        TODO: Remove

    """
    
    if label_src == 'subfolder':
        # labels from subfolder
        labels = torch.LongTensor(labels)
        one_hot_idx = torch.eye(torch.max(labels)+1)
        labels = torch.squeeze(one_hot_idx[labels])
        labels = np.asarray(labels, dtype=np.float32)
    elif os.path.exists(label_src):
        try:
            df = pd.read_csv(label_src, )
        except pd.errors.ParserError as err:
            print(f'Error reading weak labels: {err}')
            exit()

        labels = df.loc[:, ~df.columns.isin(['filename'])].to_numpy(dtype=np.float32)
        labels_fnames = df['filename'].values.tolist()
        labels_fnames, labels = self.align_labels_with_embeddings(fnames, labels_fnames, labels)
        labels = normalize(labels, norm='l2', copy=False)

    embeddings = np.asarray(embeddings, dtype=np.float32)
    labels = np.asarray(labels, dtype=np.float32)

    if label_src != '' and label_src != None:
        all_min = np.min(embeddings, axis=0)
        all_max = np.max(embeddings, axis=0)
        mean_spread = np.mean(all_max - all_min)
        labels = labels * (mean_spread * 0.5)  # 0.5 because full mean_spread seems a bit too strong
        print(
            f'[{datetime.now().strftime("%H:%M:%S.%f")}] Using {embeddings.shape[1]}-dim '
            f'embedding and {labels.shape[1]}-dim weak-labels from {label_src}.',flush=True)
        if len(embeddings) != len(labels):
            print(f'Error reading weak labels: length of weak arrays ({len(labels)}) '
                  f'does not match size of embeddings derived from dataset ({len(embeddings)})')
            exit()
        embeddings = np.concatenate([embeddings, labels], axis=1)

    else:
        print(
            f'[{datetime.now().strftime("%H:%M:%S.%f")}] Using {embeddings.shape[1]}-dim embedding ',
            flush=True)
    return embeddings


def _align_weak_labels_with_embeddings(embeddings_fnames, labels_fnames, labels):
    """Helper method to sort labels based on embeddings.
    
    """
    sort_idxs = []
    for label_fname in labels_fnames:
        for idx, fname in enumerate(embeddings_fnames):
            if len(os.path.commonpath([fname, label_fname])) > 1:
                sort_idxs.append(idx)
                break
    c = list(zip(sort_idxs, labels_fnames, labels))
    c.sort(key=lambda col: col[0])
    sort_idxs, labels_fnames, labels = zip(*c)
    return list(labels_fnames), list(labels)


class BaseEmbedding(lightning.LightningModule):
    """ All trainable embeddings must inherit from BaseEmbedding.

    """

    def __init__(self, model, criterion, optimizer, dataloader):
        """ Constructor

        Args:
            model: (torch.nn.Module) 
            criterion: (torch.nn.Module)
            optimizer: (torch.optim.Optimizer)
            dataloader: (torch.utils.data.DataLoader)

        """ 

        super(BaseEmbedding, self).__init__()
        self.model = model
        self.criterion = criterion
        self.optimizer = optimizer
        self.dataloader = dataloader
        self.checkpoint = None

    def forward(self, x):
        return self.model(x)
    
    def training_step(self, batch, batch_idx):
        # TODO all datasets need labels! default to zero labels if there are none
        x, y, _ = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)
        tensorboard_logs = {'train_loss': loss}
        return {'loss': loss, 'log': tensorboard_logs}

    def configure_optimizers(self):
        return self.optimizer

    def train_dataloader(self):
        return self.dataloader
    
    def train(self, **kwargs):
        """ Train the model on the provided dataset.

        Args:
            **kwargs: pylightning_trainer arguments, examples include:
                min_epochs: (int) Minimum number of epochs to train
                max_epochs: (int) Maximum number of epochs to train
                gpus: (int) number of gpus to use
        
        Returns:
            A trained encoder, ready for embedding datasets.

        """
        trainer = pl.Trainer(**kwargs)
        trainer.fit(self)

        checkpoint_cb = trainer.checkpoint_callback
        try:
            self.checkpoint = checkpoint_cb.kth_best_model
        except:
            print('Warning: "kth_best_model" was deprecated. \
                    Using "kth_best_model_path" instead.')
            self.checkpoint = checkpoint_cb.kth_best_model_path
            
        return self

    def embed(self, *args, **kwargs):
        """ Must be implemented by classes which inherit from BaseEmbedding.

        """
        raise NotImplementedError()

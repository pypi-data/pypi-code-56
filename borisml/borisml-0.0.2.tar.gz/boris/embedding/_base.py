""" BaseEmbeddings """

import torch
import torch.nn as nn
import pytorch_lightning as pl
import pytorch_lightning.core.lightning as lightning


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

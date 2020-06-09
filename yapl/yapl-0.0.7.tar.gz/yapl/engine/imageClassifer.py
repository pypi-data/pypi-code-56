import torch
import tensorflow as tf

from ..utils.loss import AverageMeterTorch
from ..utils.accuracy import AverageBinaryAccuracyTorch

class TfEngine:
    def __init_(self, model, dataloader, config):
        self.model = model
        self.dataloader = dataloader
        self.config = config

    def loopengine(self, istraining = True):

        pass

    def fitengine(self, istraining = True):

        pass


class TorchEngine:
    def __init_(self, model, dataloader, config):
        self.model = model
        self.dataloader = dataloader
        self.config = config

    def loopengine(self, istraining = True):
        if istraining:
            model.train()
            loss_avg = AverageLossTorch()
            acc_avg = AverageBinaryAccuracyTorch()

            for (data_batch, label_batch) in dataloader:
                print(".", end='')
                data_batch = data_batch.to(self.config.DEVICE, dtype=torch.float)
                label_batch = label_batch.to(self.config.DEVICE, dtype=torch.float)
                
                self.config.OPTIMIZER.zero_grad()
                output = model(data_batch)
                
                losses = self.config.LOSS(output, label_batch.unsqueeze(1))
                losses.backward()
                self.config.OPTIMIZER.step()
                
                loss_avg.update(losses.item(), self.config.BATCH_SIZE)
                acc_avg.update(output, label_batch.unsqueeze(1))
                
                del data_batch
                del label_batch
                
                torch.cuda.empty_cache()

            return loss_avg.avg, acc_avg.avg.item()
        
        else:
